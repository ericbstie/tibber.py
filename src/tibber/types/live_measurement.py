from __future__ import annotations

"""A class representing the LiveMeasurement type from the GraphQL Tibber API."""
from typing import TYPE_CHECKING

# Import type checking modules
if TYPE_CHECKING:
    from tibber.account import Account


class LiveMeasurement:
    """A class containing the live household electricity information."""

    def __init__(self, data: dict, tibber_client: "Account"):
        self.cache: dict = data or {}
        self.tibber_client: "Account" = tibber_client

    @property
    def timestamp(self) -> str:
        """Timestamp when usage occurred"""
        return self.cache.get("timestamp")

    @property
    def power(self) -> float:
        """Consumption at the moment (Watt)"""
        return self.cache.get("power")

    @property
    def last_meter_consumption(self) -> float:
        """Last meter active import register state (kWh)"""
        return self.cache.get("lastMeterConsumption")

    @property
    def accumulated_consumption(self) -> float:
        """kWh consumed since midnight"""
        return self.cache.get("accumulatedConsumption")

    @property
    def accumulated_production(self) -> float:
        """net kWh produced since midnight"""
        return self.cache.get("accumulatedProduction")

    @property
    def accumulated_consumption_last_hour(self) -> float:
        """kWh consumed since since last hour shift"""
        return self.cache.get("accumulatedConsumptionLastHour")

    @property
    def accumulated_production_last_hour(self) -> float:
        """net kWh produced since last hour shift"""
        return self.cache.get("accumulatedProductionLastHour")

    @property
    def accumulated_cost(self) -> float:
        """Accumulated cost since midnight; requires active Tibber power deal"""
        return self.cache.get("accumulatedCost")

    @property
    def accumulated_reward(self) -> float:
        """Accumulated reward since midnight; requires active Tibber power deal"""
        return self.cache.get("accumulatedReward")

    @property
    def currency(self) -> str:
        """Currency of displayed cost; requires active Tibber power deal"""
        return self.cache.get("currency")

    @property
    def min_power(self) -> float:
        """Min consumption since midnight (Watt)"""
        return self.cache.get("minPower")

    @property
    def average_power(self) -> float:
        """Average consumption since midnight (Watt)"""
        return self.cache.get("averagePower")

    @property
    def max_power(self) -> float:
        """Peak consumption since midnight (Watt)"""
        return self.cache.get("maxPower")

    @property
    def power_production(self) -> float:
        """Net production (A-) at the moment (Watt)"""
        return self.cache.get("powerProduction")

    @property
    def power_reactive(self) -> float:
        """Reactive consumption (Q+) at the moment (kVAr)"""
        return self.cache.get("powerReactive")

    @property
    def power_production_reactive(self) -> float:
        """Net reactive production (Q-) at the moment (kVAr)"""
        return self.cache.get("powerProductionReactive")

    @property
    def min_power_production(self) -> float:
        """Min net production since midnight (Watt)"""
        return self.cache.get("minPowerProduction")

    @property
    def max_power_production(self) -> float:
        """Max net production since midnight (Watt)"""
        return self.cache.get("maxPowerProduction")

    @property
    def last_meter_production(self) -> float:
        """Last meter active export register state (kWh)"""
        return self.cache.get("lastMeterProduction")

    @property
    def power_factor(self) -> float:
        """Power factor (active power / apparent power)"""
        return self.cache.get("powerFactor")

    @property
    def voltage_phase_1(self) -> float:
        """Voltage on phase 1; on Kaifa and Aidon meters the value is not part
        of every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("voltagePhase1")

    @property
    def voltage_phase_2(self) -> float:
        """Voltage on phase 2; on Kaifa and Aidon meters the value is not part
        of every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("voltagePhase2")

    @property
    def voltage_phase_3(self) -> float:
        """Voltage on phase 3; on Kaifa and Aidon meters the value is not part
        of every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("voltagePhase3")

    @property
    def currentL1(self) -> float:
        """Current on L1; on Kaifa and Aidon meters the value is not part of
        every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("currentL1")

    @property
    def currentL2(self) -> float:
        """Current on L2; on Kaifa and Aidon meters the value is not part of
        every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("currentL2")

    @property
    def currentL3(self) -> float:
        """Current on L3; on Kaifa and Aidon meters the value is not part of
        every HAN data frame therefore the value is null at timestamps with
        second value other than 0, 10, 20, 30, 40, 50. There can be other deviations
        based on concrete meter firmware."""
        return self.cache.get("currentL3")

    @property
    def signal_strength(self) -> int:  # pragma: no cover
        """Device signal strength (Pulse - dB; Watty - percent)"""
        return self.cache.get("signalStrength")
