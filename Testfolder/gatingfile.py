import pandas as pd
import sys

print("Python gating file started")

print("\n" + "="*50)
print("PERFORMANCE GATE REPORT")
print("="*50)

# ---------------------
# THRESHOLDS
# ---------------------

AVG_RESPONSE_TIME_MS = 100
P95_RESPONSE_TIME_MS = 500
MAX_ERROR_RATE = 0.2

# ---------------------
# READ JTL FILE
# ---------------------

df = pd.read_csv(r"D:\Git_PT\pro1\Testfolder\results.jtl")

total_requests = len(df)

failed_requests = len(
    df[df["success"].astype(str).str.lower() == "false"]
)

error_rate = (failed_requests / total_requests) * 100

avg_response_time = df["elapsed"].mean()

p95_response_time = df["elapsed"].quantile(0.95)

success_rate = 100 - error_rate

# ---------------------
# PRINT METRICS
# ---------------------

print("\n========== PERFORMANCE REPORT ==========")

print(f"Total Requests      : {total_requests}")
print(f"Failed Requests     : {failed_requests}")
print(f"Success Rate        : {success_rate:.2f}%")
print(f"Error Rate          : {error_rate:.2f}%")
print(f"Average Response    : {avg_response_time:.2f} ms")
print(f"P95 Response Time   : {p95_response_time:.2f} ms")

print("========================================\n")

# ---------------------
# GATING RULES
# ---------------------

failures = []

if avg_response_time > AVG_RESPONSE_TIME_MS:
    failures.append(
        f"Average Response Time exceeded {AVG_RESPONSE_TIME_MS} ms"
    )

if p95_response_time > P95_RESPONSE_TIME_MS:
    failures.append(
        f"P95 Response Time exceeded {P95_RESPONSE_TIME_MS} ms"
    )

if error_rate > MAX_ERROR_RATE:
    failures.append(
        f"Error Rate exceeded {MAX_ERROR_RATE}%"
    )

# ---------------------
# FINAL DECISION
# ---------------------

if failures:

    print("\nPERFORMANCE GATE FAILED\n")

    for failure in failures:
        print(f"❌ {failure}")

    sys.exit(1)

else:

    print("\n✅ PERFORMANCE GATE PASSED")

    sys.exit(0)