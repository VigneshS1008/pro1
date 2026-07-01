import pandas as pd
import sys

print("Python gating file started")

print("\n" + "=" * 60)
print("PERFORMANCE GATE REPORT")
print("=" * 60)

# ---------------------
# THRESHOLDS
# ---------------------

AVG_RESPONSE_TIME_MS = 50
P95_RESPONSE_TIME_MS = 100
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

print("\n========== TEST EXECUTION SUMMARY ==========\n")

print(f"Total Requests          : {total_requests}")
print(f"Failed Requests         : {failed_requests}")
print(f"Success Rate            : {success_rate:.2f}%")
print(f"Error Rate              : {error_rate:.2f}%")
print(f"Average Response Time   : {avg_response_time:.2f} ms")
print(f"P95 Response Time       : {p95_response_time:.2f} ms")

print("\n========== THRESHOLDS ==========\n")

print(f"Allowed Avg Response    : {AVG_RESPONSE_TIME_MS} ms")
print(f"Allowed P95 Response    : {P95_RESPONSE_TIME_MS} ms")
print(f"Allowed Error Rate      : {MAX_ERROR_RATE}%")

print("\n============================================\n")

# ---------------------
# GATING RULES
# ---------------------

failures = []

# Average Response Time Check
if avg_response_time > AVG_RESPONSE_TIME_MS:
    failures.append(
        f"Average Response Time FAILED → Actual: {avg_response_time:.2f} ms | Threshold: {AVG_RESPONSE_TIME_MS} ms"
    )
else:
    print(
        f"✅ Average Response Time PASSED → Actual: {avg_response_time:.2f} ms | Threshold: {AVG_RESPONSE_TIME_MS} ms"
    )

# P95 Check
if p95_response_time > P95_RESPONSE_TIME_MS:
    failures.append(
        f"P95 Response Time FAILED → Actual: {p95_response_time:.2f} ms | Threshold: {P95_RESPONSE_TIME_MS} ms"
    )
else:
    print(
        f"✅ P95 Response Time PASSED → Actual: {p95_response_time:.2f} ms | Threshold: {P95_RESPONSE_TIME_MS} ms"
    )

# Error Rate Check
if error_rate > MAX_ERROR_RATE:
    failures.append(
        f"Error Rate FAILED → Actual: {error_rate:.2f}% | Threshold: {MAX_ERROR_RATE}%"
    )
else:
    print(
        f"✅ Error Rate PASSED → Actual: {error_rate:.2f}% | Threshold: {MAX_ERROR_RATE}%"
    )

# ---------------------
# FINAL DECISION
# ---------------------

if failures:

    print("\n" + "=" * 60)
    print("❌ PERFORMANCE GATE FAILED")
    print("=" * 60)

    print("\nFailure Reasons:\n")

    for failure in failures:
        print(f"❌ {failure}")

    print("\nBuild Status : FAILED")

    sys.exit(1)

else:

    print("\n" + "=" * 60)
    print("✅ PERFORMANCE GATE PASSED")
    print("=" * 60)

    print("\nBuild Status : SUCCESS")

    sys.exit(0)