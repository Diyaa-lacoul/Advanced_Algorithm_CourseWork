"""
Smart Energy Grid Load Distribution Optimization (Nepal) - Procedural Approach
Greedy allocation prioritizing renewable sources with ±10% flexibility

This implementation uses greedy allocation: prioritize Solar, then Hydro, then Diesel.
Handles hourly constraints and validates source availability times.
"""

def allocate_energy_greedy():
    """
    Main greedy allocation function for energy distribution across districts.
    Returns allocation results, cost tracking, and utilization metrics.
    """
    
    # Energy demand by hour and district (kWh)
    hourly_demand = {
        "06": {"A": 20, "B": 15, "C": 25},
        "07": {"A": 22, "B": 16, "C": 28},
        "08": {"A": 25, "B": 18, "C": 30},
        "12": {"A": 28, "B": 20, "C": 32},
        "18": {"A": 30, "B": 22, "C": 35},
        "19": {"A": 35, "B": 25, "C": 40},
        "20": {"A": 32, "B": 24, "C": 38},
        "23": {"A": 26, "B": 19, "C": 28},
    }
    
    # Energy sources with specifications
    # (name, capacity, start_hour, end_hour, cost_per_kwh)
    energy_sources = [
        ("Solar", 50, 6, 18, 1.0),
        ("Hydro", 40, 0, 24, 1.5),
        ("Diesel", 60, 17, 23, 3.0),
    ]
    
    districts = ["A", "B", "C"]
    allocation_log = []
    total_cost = 0.0
    total_energy_used = 0.0
    renewable_energy = 0.0
    diesel_usage_log = []
    
    # Process each hour
    for hour_str in sorted(hourly_demand.keys()):
        hour = int(hour_str)
        hour_allocation = {"hour": hour_str, "districts": {}}
        hour_demand = hourly_demand[hour_str]
        
        # Calculate total demand for this hour
        total_hour_demand = sum(hour_demand.values())
        hour_cost = 0.0
        hour_energy_used = 0.0
        
        # Available sources for this hour (in priority order: cheapest first)
        available_sources = []
        for source_name, capacity, start_h, end_h, cost in energy_sources:
            # Validate source availability
            if start_h <= hour < end_h:
                available_sources.append((source_name, capacity, cost))
        
        # Sort by cost (greedy: cheapest first)
        available_sources.sort(key=lambda x: x[2])
        
        # Allocate energy to districts
        remaining_demand = total_hour_demand
        district_allocation = {d: 0 for d in districts}
        source_breakdown = {d: {} for d in districts}
        
        # Greedy allocation: use sources in cost order
        for source_name, capacity, cost in available_sources:
            source_used = 0
            
            # Distribute from this source proportionally to districts
            for district in districts:
                if remaining_demand <= 0.01:
                    break
                
                district_proportion = hour_demand[district] / total_hour_demand if total_hour_demand > 0 else 0
                allocation_for_district = min(
                    district_proportion * capacity,
                    hour_demand[district] - district_allocation[district]
                )
                
                district_allocation[district] += allocation_for_district
                source_used += allocation_for_district
                
                if source_name not in source_breakdown[district]:
                    source_breakdown[district][source_name] = 0
                source_breakdown[district][source_name] += allocation_for_district
            
            remaining_demand -= source_used
            hour_energy_used += source_used
            hour_cost += source_used * cost
            
            # Track renewable energy
            if source_name in ["Solar", "Hydro"]:
                renewable_energy += source_used
            elif source_name == "Diesel":
                diesel_usage_log.append({
                    "hour": hour,
                    "amount": source_used,
                    "reason": "Peak demand or insufficient renewables"
                })
        
        # Demand met percentage with ±10% flexibility
        demand_met_pct = (hour_energy_used / total_hour_demand * 100) if total_hour_demand > 0 else 0
        flexibility_lower = 90.0
        flexibility_upper = 110.0
        is_demand_satisfied = flexibility_lower <= demand_met_pct <= flexibility_upper
        
        # Record allocation
        for district in districts:
            hour_allocation["districts"][district] = {
                "allocated": round(district_allocation[district], 2),
                "demand": hour_demand[district],
                "sources": source_breakdown[district]
            }
        
        hour_allocation["total_used"] = round(hour_energy_used, 2)
        hour_allocation["total_demand"] = total_hour_demand
        hour_allocation["demand_met_pct"] = round(demand_met_pct, 1)
        hour_allocation["satisfied"] = is_demand_satisfied
        hour_allocation["cost"] = round(hour_cost, 2)
        
        allocation_log.append(hour_allocation)
        total_cost += hour_cost
        total_energy_used += hour_energy_used
    
    return {
        "allocations": allocation_log,
        "total_cost_rs": round(total_cost, 2),
        "total_energy_kwh": round(total_energy_used, 2),
        "renewable_percentage": round((renewable_energy / total_energy_used * 100) if total_energy_used > 0 else 0, 1),
        "diesel_usage_log": diesel_usage_log
    }


def print_results_table(results):
    """Print formatted results table."""
    print("\n" + "="*100)
    print("SMART ENERGY GRID LOAD DISTRIBUTION - HOURLY ALLOCATION REPORT")
    print("="*100)
    print(f"{'Hour':<6} {'District':<10} {'Solar':<8} {'Hydro':<8} {'Diesel':<8} {'Total Used':<12} {'Demand':<10} {'% Met':<8} {'Status':<12}")
    print("-"*100)
    
    for allocation in results["allocations"]:
        hour = allocation["hour"]
        districts_data = allocation["districts"]
        
        for i, district in enumerate(["A", "B", "C"]):
            data = districts_data[district]
            sources = data["sources"]
            solar = sources.get("Solar", 0)
            hydro = sources.get("Hydro", 0)
            diesel = sources.get("Diesel", 0)
            total_used = data["allocated"]
            demand = data["demand"]
            
            if i == 0:
                status = "✓ OK" if allocation["satisfied"] else "✗ UNMET"
                print(f"{hour:<6} {district:<10} {solar:<8.1f} {hydro:<8.1f} {diesel:<8.1f} {total_used:<12.2f} {demand:<10.0f} {allocation['demand_met_pct']:<8.1f} {status:<12}")
            else:
                print(f"{'':6} {district:<10} {solar:<8.1f} {hydro:<8.1f} {diesel:<8.1f} {total_used:<12.2f} {demand:<10.0f}")
    
    print("="*100)


def print_analysis_report(results):
    """Print analysis summary report."""
    print("\nANALYSIS REPORT")
    print("-" * 50)
    print(f"Total Distribution Cost: Rs. {results['total_cost_rs']:.2f}")
    print(f"Total Energy Used: {results['total_energy_kwh']:.2f} kWh")
    print(f"Renewable Energy Percentage: {results['renewable_percentage']:.1f}%")
    print(f"Diesel Usage Count: {len(results['diesel_usage_log'])} instances")
    
    if results["diesel_usage_log"]:
        print("\nDiesel Utilization Log:")
        for entry in results["diesel_usage_log"]:
            print(f"  Hour {entry['hour']}: {entry['amount']:.2f} kWh - {entry['reason']}")


if __name__ == "__main__":
    results = allocate_energy_greedy()
    print_results_table(results)
    print_analysis_report(results)
