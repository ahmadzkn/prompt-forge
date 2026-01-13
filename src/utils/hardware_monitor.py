import psutil
import GPUtil
import platform
from typing import Dict, Any

class HardwareMonitor:
    @staticmethod
    def get_system_stats() -> Dict[str, Any]:
        stats = {
            "cpu_percent": psutil.cpu_percent(interval=None),
            "ram_percent": psutil.virtual_memory().percent,
            "gpu_found": False,
            "gpus": []
        }
        
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                stats["gpu_found"] = True
                for gpu in gpus:
                    stats["gpus"].append({
                        "name": gpu.name,
                        "load": f"{gpu.load * 100:.1f}%",
                        "memory_used": f"{gpu.memoryUsed}MB",
                        "memory_total": f"{gpu.memoryTotal}MB",
                        "temperature": f"{gpu.temperature}C"
                    })
        except Exception:
            # GPUtil might fail if no NVIDIA drivers or on Mac
            pass
            
        return stats

    @staticmethod
    def is_gpu_available() -> bool:
        try:
            return len(GPUtil.getGPUs()) > 0
        except:
            return False
