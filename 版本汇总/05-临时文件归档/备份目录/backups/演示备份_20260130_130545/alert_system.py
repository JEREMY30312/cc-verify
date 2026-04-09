#!/usr/bin/env python3
"""
警报系统
用于检测和发送阶段C验证系统的警报
"""

import json
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import sys

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("alert_system.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)


class AlertSystem:
    """警报系统"""

    def __init__(self, config_file: str = "alert_config.json"):
        """
        初始化警报系统

        Args:
            config_file: 配置文件路径
        """
        self.config = self.load_config(config_file)
        self.alert_history = self.load_alert_history()
        self.alert_rules = self.load_alert_rules()

    def load_config(self, config_file: str) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipients": [],
            },
            "slack": {
                "enabled": False,
                "webhook_url": "",
            },
            "alert_thresholds": {
                "simplification_rate": {
                    "critical_low": 0.04,  # 低于4%
                    "critical_high": 0.16,  # 高于16%
                    "warning_low": 0.05,  # 低于5%
                    "warning_high": 0.15,  # 高于15%
                },
                "p1_preservation": {
                    "critical": 0.98,  # 低于98%
                    "warning": 0.99,  # 低于99%
                },
                "p2_preservation": {
                    "critical": 0.80,  # 低于80%
                    "warning": 0.85,  # 低于85%
                },
                "quality_degradation": {
                    "critical": 0.15,  # 高于15%
                    "warning": 0.10,  # 高于10%
                },
                "error_rate": {
                    "critical": 0.30,  # 高于30%
                    "warning": 0.10,  # 高于10%
                },
                "consecutive_failures": {
                    "critical": 5,  # 连续5次失败
                    "warning": 3,  # 连续3次失败
                },
            },
            "notification_settings": {
                "send_immediate_alerts": True,
                "daily_summary": True,
                "weekly_report": True,
                "alert_cooldown_minutes": 30,  # 相同警报冷却时间
            },
        }

        try:
            if Path(config_file).exists():
                with open(config_file, "r", encoding="utf-8") as f:
                    user_config = json.load(f)
                    # 合并配置
                    self.merge_config(default_config, user_config)
            return default_config
        except Exception as e:
            logger.error(f"加载配置文件失败，使用默认配置: {e}")
            return default_config

    def merge_config(self, default: Dict, user: Dict):
        """合并配置"""
        for key, value in user.items():
            if (
                key in default
                and isinstance(default[key], dict)
                and isinstance(value, dict)
            ):
                self.merge_config(default[key], value)
            else:
                default[key] = value

    def load_alert_history(self) -> List[Dict[str, Any]]:
        """加载警报历史"""
        try:
            history_file = Path("alert_history.json")
            if history_file.exists():
                with open(history_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"加载警报历史失败: {e}")
            return []

    def save_alert_history(self):
        """保存警报历史"""
        try:
            history_file = Path("alert_history.json")
            with open(history_file, "w", encoding="utf-8") as f:
                json.dump(self.alert_history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"保存警报历史失败: {e}")

    def load_alert_rules(self) -> Dict[str, Any]:
        """加载警报规则"""
        return {
            "simplification_rate_out_of_range": {
                "description": "精简率超出目标范围",
                "severity": "critical",
                "condition": lambda data: (
                    data.get("avg_simplification_rate", 0) < 0.04
                    or data.get("avg_simplification_rate", 0) > 0.16
                ),
                "message_template": "精简率严重异常: {avg_simplification_rate:.1%} (目标: 7.9% ± 12%)",
            },
            "simplification_rate_warning": {
                "description": "精简率接近边界",
                "severity": "warning",
                "condition": lambda data: (
                    (0.04 <= data.get("avg_simplification_rate", 0) < 0.05)
                    or (0.15 < data.get("avg_simplification_rate", 0) <= 0.16)
                ),
                "message_template": "精简率接近边界: {avg_simplification_rate:.1%}",
            },
            "p1_preservation_critical": {
                "description": "P1元素保留率严重不足",
                "severity": "critical",
                "condition": lambda data: (data.get("p1_avg_ratio", 0) < 0.98),
                "message_template": "P1元素保留率严重不足: {p1_avg_ratio:.1%} (目标: 100%)",
            },
            "p1_preservation_warning": {
                "description": "P1元素保留率不足",
                "severity": "warning",
                "condition": lambda data: (0.98 <= data.get("p1_avg_ratio", 0) < 0.99),
                "message_template": "P1元素保留率不足: {p1_avg_ratio:.1%}",
            },
            "p2_preservation_critical": {
                "description": "P2元素保留率严重不足",
                "severity": "critical",
                "condition": lambda data: (data.get("p2_avg_ratio", 0) < 0.80),
                "message_template": "P2元素保留率严重不足: {p2_avg_ratio:.1%} (目标: ≥90%)",
            },
            "p2_preservation_warning": {
                "description": "P2元素保留率不足",
                "severity": "warning",
                "condition": lambda data: (0.80 <= data.get("p2_avg_ratio", 0) < 0.85),
                "message_template": "P2元素保留率不足: {p2_avg_ratio:.1%}",
            },
            "quality_degradation_critical": {
                "description": "质量下降严重",
                "severity": "critical",
                "condition": lambda data: (
                    data.get("avg_quality_degradation", 0) > 0.15
                ),
                "message_template": "质量下降严重: {avg_quality_degradation:.1%} (目标: ≤8%)",
            },
            "quality_degradation_warning": {
                "description": "质量下降过高",
                "severity": "warning",
                "condition": lambda data: (
                    0.10 < data.get("avg_quality_degradation", 0) <= 0.15
                ),
                "message_template": "质量下降过高: {avg_quality_degradation:.1%}",
            },
            "high_error_rate": {
                "description": "错误率过高",
                "severity": "warning",
                "condition": lambda data: (data.get("error_rate", 0) > 0.10),
                "message_template": "错误率过高: {error_rate:.1%}",
            },
            "critical_error_rate": {
                "description": "错误率严重过高",
                "severity": "critical",
                "condition": lambda data: (data.get("error_rate", 0) > 0.30),
                "message_template": "错误率严重过高: {error_rate:.1%}",
            },
            "user_perception_negative": {
                "description": "用户感知负面反馈过多",
                "severity": "warning",
                "condition": lambda data: (data.get("negative_keyword_count", 0) >= 3),
                "message_template": "检测到 {negative_keyword_count} 次负面用户反馈关键词",
            },
        }

    def analyze_validation_result(
        self, validation_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """分析验证结果并生成警报"""
        alerts = []

        # 提取数据
        checks = validation_result.get("detailed_checks", {})
        stats = validation_result.get("statistics", {})

        # 准备分析数据
        analysis_data = {
            "batch_id": validation_result.get("batch_id", "unknown"),
            "validation_time": validation_result.get("validation_time", ""),
            "overall_status": validation_result.get("overall_status", "unknown"),
        }

        # 精简率数据
        simpl_check = checks.get("phase_c_simplification_rate", {})
        if simpl_check.get("status") != "no_data":
            analysis_data["avg_simplification_rate"] = simpl_check.get(
                "avg_simplification_rate", 0
            )

        # P1/P2保留率数据
        p1p2_check = checks.get("phase_c_p1_p2_preservation", {})
        p1_pres = p1p2_check.get("p1_preservation", {})
        if p1_pres:
            analysis_data["p1_avg_ratio"] = p1_pres.get("avg_ratio", 0)

        p2_pres = p1p2_check.get("p2_preservation", {})
        if p2_pres:
            analysis_data["p2_avg_ratio"] = p2_pres.get("avg_ratio", 0)

        # 质量下降数据
        quality_check = checks.get("phase_c_quality_degradation", {})
        quality_stats = quality_check.get("quality_degradation_stats", {})
        if quality_stats:
            analysis_data["avg_quality_degradation"] = quality_stats.get(
                "avg_degradation", 0
            )

        # 错误率数据
        error_check = checks.get("error_analysis", {})
        if error_check.get("status") != "no_data":
            error_examples = error_check.get("error_examples_count", 0)
            total_examples = stats.get("total_examples", 1)
            analysis_data["error_rate"] = error_examples / total_examples

        # 用户感知数据
        user_check = checks.get("phase_c_user_perception", {})
        user_stats = user_check.get("user_perception_stats", {})
        if user_stats:
            analysis_data["negative_keyword_count"] = user_stats.get(
                "total_keyword_occurrences", 0
            )

        # 应用所有警报规则
        for rule_name, rule in self.alert_rules.items():
            try:
                if rule["condition"](analysis_data):
                    alert = {
                        "rule_name": rule_name,
                        "description": rule["description"],
                        "severity": rule["severity"],
                        "message": rule["message_template"].format(**analysis_data),
                        "batch_id": analysis_data["batch_id"],
                        "timestamp": analysis_data["validation_time"],
                        "data": {
                            k: v
                            for k, v in analysis_data.items()
                            if k not in ["batch_id", "validation_time"]
                        },
                    }
                    alerts.append(alert)
            except Exception as e:
                logger.error(f"应用警报规则 {rule_name} 失败: {e}")

        return alerts

    def check_alert_cooldown(self, alert: Dict[str, Any]) -> bool:
        """检查警报冷却时间"""
        cooldown_minutes = self.config["notification_settings"][
            "alert_cooldown_minutes"
        ]
        if cooldown_minutes <= 0:
            return True  # 无冷却时间

        recent_alerts = [
            a
            for a in self.alert_history
            if a.get("rule_name") == alert["rule_name"]
            and a.get("batch_id") == alert["batch_id"]
        ]

        if not recent_alerts:
            return True

        # 检查最近是否有相同警报
        latest_alert = max(recent_alerts, key=lambda x: x.get("timestamp", ""))
        latest_time = datetime.strptime(latest_alert["timestamp"], "%Y-%m-%d %H:%M:%S")
        current_time = datetime.strptime(alert["timestamp"], "%Y-%m-%d %H:%M:%S")

        time_diff = (current_time - latest_time).total_seconds() / 60  # 分钟

        return time_diff >= cooldown_minutes

    def send_email_alert(self, alert: Dict[str, Any]):
        """发送电子邮件警报"""
        if not self.config["email"]["enabled"]:
            return

        try:
            email_config = self.config["email"]

            msg = MIMEMultipart()
            msg["From"] = email_config["sender_email"]
            msg["To"] = ", ".join(email_config["recipients"])
            msg["Subject"] = (
                f"[{alert['severity'].upper()}] 阶段C验证系统警报 - {alert['batch_id']}"
            )

            body = f"""
阶段C验证系统检测到{alert["severity"]}级别警报

警报详情:
- 规则: {alert["description"]}
- 批次ID: {alert["batch_id"]}
- 时间: {alert["timestamp"]}
- 严重程度: {alert["severity"]}

警报消息:
{alert["message"]}

相关数据:
{json.dumps(alert["data"], ensure_ascii=False, indent=2)}

请及时检查处理。
"""

            msg.attach(MIMEText(body, "plain", "utf-8"))

            with smtplib.SMTP(
                email_config["smtp_server"], email_config["smtp_port"]
            ) as server:
                server.starttls()
                server.login(
                    email_config["sender_email"], email_config["sender_password"]
                )
                server.send_message(msg)

            logger.info(f"电子邮件警报已发送: {alert['rule_name']}")

        except Exception as e:
            logger.error(f"发送电子邮件警报失败: {e}")

    def send_alert(self, alert: Dict[str, Any]):
        """发送警报"""
        # 检查冷却时间
        if not self.check_alert_cooldown(alert):
            logger.info(f"警报 {alert['rule_name']} 仍在冷却中，跳过发送")
            return

        # 记录到历史
        self.alert_history.append(alert)
        self.save_alert_history()

        # 发送通知
        if self.config["notification_settings"]["send_immediate_alerts"]:
            if alert["severity"] == "critical":
                self.send_email_alert(alert)

            # 控制台输出
            icon = "🔴" if alert["severity"] == "critical" else "🟡"
            print(f"\n{icon} 警报: {alert['message']}")
            print(f"   规则: {alert['description']}")
            print(f"   批次: {alert['batch_id']}")
            print(f"   时间: {alert['timestamp']}")

        logger.info(f"警报已处理: {alert['rule_name']} - {alert['severity']}")

    def process_validation_result(self, validation_result: Dict[str, Any]):
        """处理验证结果"""
        alerts = self.analyze_validation_result(validation_result)

        if not alerts:
            logger.info("未检测到警报")
            return

        # 按严重程度排序
        alerts.sort(key=lambda x: 0 if x["severity"] == "critical" else 1)

        # 发送警报
        for alert in alerts:
            self.send_alert(alert)

        return alerts

    def generate_daily_summary(self):
        """生成每日摘要"""
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

        today_alerts = [
            a for a in self.alert_history if a["timestamp"].startswith(today)
        ]
        yesterday_alerts = [
            a for a in self.alert_history if a["timestamp"].startswith(yesterday)
        ]

        summary = {
            "date": today,
            "today_alerts": len(today_alerts),
            "yesterday_alerts": len(yesterday_alerts),
            "critical_alerts_today": len(
                [a for a in today_alerts if a["severity"] == "critical"]
            ),
            "warning_alerts_today": len(
                [a for a in today_alerts if a["severity"] == "warning"]
            ),
            "top_rules_today": {},
        }

        # 统计今天最常触发的规则
        rule_counts = {}
        for alert in today_alerts:
            rule_name = alert["rule_name"]
            rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1

        if rule_counts:
            top_rules = sorted(rule_counts.items(), key=lambda x: x[1], reverse=True)[
                :5
            ]
            summary["top_rules_today"] = dict(top_rules)

        return summary


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description="阶段C验证系统警报系统")
    parser.add_argument("validation_file", help="验证结果文件路径")
    parser.add_argument("--config", default="alert_config.json", help="配置文件路径")
    parser.add_argument("--test", action="store_true", help="测试模式，不发送实际通知")

    args = parser.parse_args()

    alert_system = AlertSystem(args.config)

    if args.test:
        alert_system.config["email"]["enabled"] = False
        alert_system.config["slack"]["enabled"] = False
        print("测试模式启用，不会发送实际通知")

    try:
        with open(args.validation_file, "r", encoding="utf-8") as f:
            validation_result = json.load(f)

        alerts = alert_system.process_validation_result(validation_result)

        if alerts:
            print(f"\n✅ 检测到 {len(alerts)} 个警报")
            for alert in alerts:
                icon = "🔴" if alert["severity"] == "critical" else "🟡"
                print(f"{icon} {alert['message']}")
        else:
            print("✅ 未检测到警报")

    except Exception as e:
        logger.error(f"处理验证结果失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
