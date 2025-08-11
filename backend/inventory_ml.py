def optimize_inventory(max_space, items):
    """
    Optimize inventory allocation based on value per cubic meter.

    Args:
        max_space (float): Total available storage space in cubic meters.
        items (list[dict]): Each dict must contain:
            - Region_Name (str)
            - Predicted_Quantity (int)
            - Space_Per_Unit (float)
            - Value_Per_Unit (float)

    Returns:
        dict: {
            'max_space': float,
            'remaining_space': float,
            'total_value': float,
            'allocation': list[dict]
        }
    """

    if not isinstance(max_space, (int, float)) or max_space <= 0:
        raise ValueError("max_space must be a positive number.")

    if not isinstance(items, list) or not items:
        raise ValueError("items must be a non-empty list.")

    required_keys = {"Region_Name", "Predicted_Quantity", "Space_Per_Unit", "Value_Per_Unit"}

    # Validate items
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} must be a dictionary.")

        missing_keys = required_keys - item.keys()
        if missing_keys:
            raise ValueError(f"Item at index {idx} is missing keys: {missing_keys}")

        if item["Space_Per_Unit"] <= 0:
            raise ValueError(f"Space_Per_Unit must be > 0 for region {item['Region_Name']}")

        if item["Predicted_Quantity"] < 0:
            raise ValueError(f"Predicted_Quantity must be >= 0 for region {item['Region_Name']}")

        if item["Value_Per_Unit"] < 0:
            raise ValueError(f"Value_Per_Unit must be >= 0 for region {item['Region_Name']}")

    # Calculate value per cubic meter
    for item in items:
        item["Value_Per_m3"] = item["Value_Per_Unit"] / item["Space_Per_Unit"]

    # Sort by best value density
    sorted_items = sorted(items, key=lambda x: x["Value_Per_m3"], reverse=True)

    remaining_space = max_space
    allocation = []

    for item in sorted_items:
        # Determine how many units fit in remaining space
        max_units_that_fit = int(remaining_space // item["Space_Per_Unit"])
        units_to_store = min(max_units_that_fit, item["Predicted_Quantity"])

        if units_to_store > 0:
            space_used = units_to_store * item["Space_Per_Unit"]
            value_gained = units_to_store * item["Value_Per_Unit"]

            allocation.append({
                "Region_Name": item["Region_Name"],
                "Units_Allocated": units_to_store,
                "Space_Used": round(space_used, 2),
                "Value": round(value_gained, 2),
                "Value_Per_m3": round(item["Value_Per_m3"], 2)
            })

            remaining_space -= space_used

        if remaining_space <= 0:
            break  # stop if no space left

    total_value = sum(a["Value"] for a in allocation)

    return {
        "max_space": max_space,
        "remaining_space": round(remaining_space, 2),
        "total_value": round(total_value, 2),
        "allocation": allocation
    }
