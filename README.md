# Real-Time Fraud Detection Pipeline

Personal reference notes — architecture + key decisions. Expand into a full README later.

## Motivation

Sparked by a question to a Barclays MD about payments resilience during a team session —
his answer on how hard payments outages are to prevent led me to look into payments
engineering more broadly. Landed on fraud detection because it combines two hard problems:
high-throughput streaming and real-time ML inference under a strict latency budget.

## Goal

Sustain **1000 transactions/sec** with **sub-second end-to-end latency (P99)** from
transaction ingestion to a published decision.

## Architecture

```
Historical dataset (PaySim)
        |  replayed per-card in order, concurrent across cards
        v
+-------------------------+
| Async Python producer    |   Poisson-ish pacing, rate_multiplier controls load
+-------------------------+
        |
        v
+-------------------------+
| Kafka: transactions.raw  |   partitioned by card_id (12 partitions)
+-------------------------+
        |
        v
+-------------------------------+
| Python feature engineering     |  windowing/sequence assembly per card
| (manual consumer, Redis-backed |  Redis: capped list per card_id
| sliding window)                |  (online feature store, LPUSH+LTRIM)
+-------------------------------+
        |
        v
+-------------------------------+
| Kafka: transactions.enriched   |  fixed-length sequence + normalized features
+-------------------------------+
        |
        v
+-------------------------------+
| FastAPI inference service      |  micro-batches (size/time threshold)
| LSTM over raw transaction seq  |  one batched forward pass per flush
+-------------------------------+
        |
        v
+-------------------------------+
| Kafka: fraud.scored            |
+-------------------------------+
        |
        v
+-------------------------------+
| Spring Boot decision service   |  rules + ML score -> block/approve
| (Kafka consumer, manual ack)   |  audit write to Postgres (unique on txn_id)
+-------------------------------+        |
        |                                v
        |                        Postgres: audit trail
        |                        + REST API for analyst case review
        v
+-------------------------------+
| Kafka: payment.blocked/approved|
+-------------------------------+
        |
        v
   Downstream consumers (dashboard, alerting)
```

All hops are Kafka — no synchronous RPC between services. Each service is its own
consumer group and scales independently.

## Tech stack

- **Producer**: Python, `confluent-kafka` / `aiokafka`, PaySim dataset replay
- **Feature engineering**: Python, manual windowing (deque/Redis-backed), no framework
  initially — may swap to Bytewax later
- **State store**: Redis — capped list per `card_id`, used as a real-time online
  feature store (this is a legitimate production pattern, not a simplification)
- **Inference**: FastAPI, LSTM over raw (normalized) transaction sequences, micro-batched
- **Decisioning**: Spring Boot, Kafka consumer with manual ack, rules layered on ML score
- **Persistence**: Postgres — append-only audit trail, idempotent on `transaction_id`
- **Infra**: Docker Compose, Kafka in KRaft mode (no Zookeeper)
- **Observability**: Prometheus + Grafana — consumer lag, end-to-end latency (P50/P95/P99),
  batch size vs. throughput

## Key design decisions

- **Partition key = `card_id`** everywhere — guarantees per-card ordering and lets windowed
  state live on a single instance with no cross-instance coordination.
- **Offset commit only after downstream success** (publish / DB write) — at-least-once
  delivery, reprocessing on crash is expected and handled via idempotent writes, not avoided.
- **Redis over Celery/task queue** — Kafka already provides the decoupling/backpressure a
  task queue would give; Redis here is a state store, not a broker.
- **Dropped gRPC between Spring Boot and FastAPI** — kept Kafka end-to-end instead, to avoid
  reintroducing a synchronous failure/duplicate-scoring window. Considered Avro/Schema
  Registry instead if a serialization-efficiency story is wanted later.
- **Raw-sequence LSTM input over hand-engineered aggregate features** — deliberate tradeoff:
  less feature engineering work, more model tuning work (class imbalance, sequence
  length/padding). Explainability is weaker than a rules-based feature approach — acceptable
  here since Spring Boot's rule layer covers the explainability need for blocking decisions.
- **PaySim over synthetic generator** — real dataset with ground-truth labels and existing
  temporal structure (`step`, `nameOrig`/`nameDest`); replay must preserve per-card order
  even while randomizing/controlling concurrent load across cards.

## Open / to decide

- Partition + instance counts for feature engineering and FastAPI services specifically
- Final call: manual consumer vs. Bytewax for windowing
- LSTM architecture details: sequence length, padding strategy, class imbalance handling
- Load test plan: ramp schedule, instance-count sweep, what to graph for the README write-up
