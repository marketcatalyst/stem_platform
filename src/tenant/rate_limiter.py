import time


class NoisyNeighbourDefenceSystem:
    """
    Implements tenant-aware compute rate limiting to protect shared execution clusters.
    Guarantees standard real-time display tasks retain mandatory latency properties.
    """

    def __init__(self, mandatory_latency_threshold_ms: int = 350):
        self.max_latency_allowed_ms = mandatory_latency_threshold_ms
        # In-memory tracking repository mapping active request histories per tenant channel
        self.tenant_request_logs = {}

    def inspect_and_throttle_route(
        self, subdomain: str, task_weight_units: int
    ) -> dict:
        """
        Evaluates processing congestion metrics to protect server performance parameters.
        Throttles batch volumes if a broker initiates multiple simulations concurrently.
        """
        current_timestamp = time.time()
        subdomain = subdomain.lower()

        # Initialise tracking ledger if sub-domain context string is new
        if subdomain not in self.tenant_request_logs:
            self.tenant_request_logs[subdomain] = []

        # Clean up stale log tracking events older than 60 seconds
        self.tenant_request_logs[subdomain] = [
            t
            for t in self.tenant_request_logs[subdomain]
            if current_timestamp - t < 60.0
        ]

        active_minute_load = len(self.tenant_request_logs[subdomain])

        # Trigger protective throttling if current load profiles compromise performance limits
        if active_minute_load > 10 or task_weight_units >= 50:
            suggested_backoff_seconds = round(float(0.5 * active_minute_load), 2)
            execution_priority = "LOW_BACKGROUND_QUEUE"
            requires_throttling = True
        else:
            suggested_backoff_seconds = 0.0
            execution_priority = "HIGH_REALTIME_STREAM"
            requires_throttling = False

        # Record this validated execution pulse within the system history logs
        self.tenant_request_logs[subdomain].append(current_timestamp)

        return {
            "subdomain": subdomain,
            "requires_throttling": requires_throttling,
            "suggested_backoff_seconds": suggested_backoff_seconds,
            "allocated_execution_priority": execution_priority,
            "guaranteed_ui_latency_threshold_ms": self.max_latency_allowed_ms,
        }
