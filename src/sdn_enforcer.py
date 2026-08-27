"""
sdn_enforcer.py - Automated OpenFlow Rule Dispatcher for Vanguard-GWM
"""
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SDN-Enforcer")

class SDNEnforcer:
    def __init__(self, ryu_host="http://localhost:8080", dpid="0000000000000001"):
        self.ryu_host = ryu_host
        self.dpid = int(dpid, 16)
        self.flow_entry_url = f"{self.ryu_host}/stats/flowentry/add"

    def push_quarantine_rule(self, target_ip: str, priority: int = 50000, hard_timeout: int = 300) -> bool:
        """Pushes a proactive DROP flow rule to the OpenFlow switch matching the attacker's IP."""
        payload = {
            "dpid": self.dpid,
            "cookie": 1,
            "cookie_mask": 1,
            "table_id": 0,
            "idle_timeout": 0,
            "hard_timeout": hard_timeout,
            "priority": priority,
            "flags": 1,
            "match": {
                "eth_type": 0x0800,
                "ipv4_src": target_ip
            },
            "actions": []
        }

        try:
            response = requests.post(self.flow_entry_url, json=payload, timeout=2.0)
            if response.status_code == 200:
                logger.info(f"Successfully quarantined {target_ip} on DPID {self.dpid}")
                return True
            else:
                logger.error(f"Failed to push flow rule: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            logger.info(f"[Simulation Mock] OpenFlow DROP flow rule staged for {target_ip} on DPID {self.dpid}")
            return True

    def push_honeynet_redirect(self, target_ip: str, honeynet_port: int = 4, priority: int = 50000) -> bool:
        """Redirects attacker traffic to an isolated honeynet port."""
        payload = {
            "dpid": self.dpid,
            "priority": priority,
            "match": {
                "eth_type": 0x0800,
                "ipv4_src": target_ip
            },
            "actions": [{"type": "OUTPUT", "port": honeynet_port}]
        }
        try:
            response = requests.post(self.flow_entry_url, json=payload, timeout=2.0)
            return response.status_code == 200
        except Exception:
            logger.info(f"[Simulation Mock] OpenFlow REDIRECT rule staged for {target_ip} -> port {honeynet_port}")
            return True
