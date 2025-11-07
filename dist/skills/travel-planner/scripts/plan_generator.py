#!/usr/bin/env python3
"""
Travel Plan Generator

Generates detailed travel plans including itinerary, budget, and checklists.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from travel_db import get_preferences, add_trip
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List


def generate_daily_itinerary(destination: str, num_days: int,
                            interests: List[str], pace: str = "moderate") -> List[Dict[str, Any]]:
    """
    Generate a suggested daily itinerary structure.

    This is a template that should be filled with actual attractions and activities
    based on web research or user input.
    """
    itinerary = []

    activities_per_day = {
        "relaxed": 2,
        "moderate": 3,
        "packed": 4
    }

    num_activities = activities_per_day.get(pace, 3)

    for day in range(1, num_days + 1):
        day_plan = {
            "day": day,
            "date": "",  # To be filled with actual dates
            "morning": {
                "time": "9:00 AM - 12:00 PM",
                "activity": f"Activity {day}A (to be customized)",
                "type": "sightseeing",
                "duration": "3 hours",
                "notes": "Based on user interests"
            },
            "afternoon": {
                "time": "2:00 PM - 5:00 PM",
                "activity": f"Activity {day}B (to be customized)",
                "type": "experience",
                "duration": "3 hours",
                "notes": ""
            },
            "evening": {
                "time": "7:00 PM - 10:00 PM",
                "activity": f"Activity {day}C (to be customized)",
                "type": "dining",
                "duration": "2-3 hours",
                "notes": ""
            },
            "meals": {
                "breakfast": "Hotel/Local cafe",
                "lunch": "Near afternoon activity",
                "dinner": "Local restaurant recommendation"
            },
            "accommodation": "Hotel/Accommodation name"
        }

        if pace == "relaxed":
            day_plan.pop("evening")  # Fewer activities for relaxed pace

        itinerary.append(day_plan)

    return itinerary


def calculate_budget_breakdown(total_budget: float, num_days: int,
                               accommodation_level: str = "mid-range") -> Dict[str, Any]:
    """
    Generate budget breakdown by category.
    """
    # Default percentage allocations
    allocations = {
        "budget": {
            "accommodation": 0.40,
            "food": 0.25,
            "activities": 0.20,
            "transportation": 0.10,
            "miscellaneous": 0.05
        },
        "mid-range": {
            "accommodation": 0.35,
            "food": 0.25,
            "activities": 0.25,
            "transportation": 0.10,
            "miscellaneous": 0.05
        },
        "luxury": {
            "accommodation": 0.45,
            "food": 0.20,
            "activities": 0.20,
            "transportation": 0.10,
            "miscellaneous": 0.05
        }
    }

    allocation = allocations.get(accommodation_level, allocations["mid-range"])

    breakdown = {}
    for category, percentage in allocation.items():
        amount = total_budget * percentage
        per_day = amount / num_days if num_days > 0 else 0
        breakdown[category] = {
            "total": round(amount, 2),
            "per_day": round(per_day, 2),
            "percentage": percentage * 100
        }

    return {
        "total_budget": total_budget,
        "duration_days": num_days,
        "breakdown": breakdown,
        "daily_average": round(total_budget / num_days, 2) if num_days > 0 else 0
    }


def generate_packing_checklist(destination_climate: str, duration_days: int,
                               trip_activities: List[str]) -> Dict[str, List[str]]:
    """
    Generate packing checklist based on destination and activities.
    """
    checklist = {
        "essentials": [
            "Passport",
            "Visa (if required)",
            "Travel insurance documents",
            "Flight tickets/boarding passes",
            "Hotel confirmations",
            "Credit/debit cards",
            "Local currency",
            "Phone and charger",
            "Adapter/converter (if needed)",
            "Medications (prescription and basic)",
            "Copies of important documents"
        ],
        "clothing": [],
        "toiletries": [
            "Toothbrush and toothpaste",
            "Shampoo and soap",
            "Deodorant",
            "Sunscreen",
            "Any personal care items"
        ],
        "technology": [
            "Phone charger",
            "Power bank",
            "Camera (if bringing)",
            "Headphones",
            "Laptop/tablet (if needed)"
        ],
        "activities": []
    }

    # Add climate-appropriate clothing
    if "tropical" in destination_climate.lower() or "warm" in destination_climate.lower():
        checklist["clothing"].extend([
            "Lightweight, breathable clothes",
            "Shorts and t-shirts",
            "Sundress/summer clothes",
            "Swimsuit",
            "Sun hat",
            "Sunglasses",
            "Sandals/flip-flops"
        ])
    elif "cold" in destination_climate.lower() or "winter" in destination_climate.lower():
        checklist["clothing"].extend([
            "Warm jacket/coat",
            "Sweaters/hoodies",
            "Long pants",
            "Thermal underwear",
            "Warm socks",
            "Gloves and scarf",
            "Winter boots"
        ])
    else:  # Moderate/temperate
        checklist["clothing"].extend([
            "Mix of light and warm layers",
            "T-shirts and long-sleeve shirts",
            "Pants and shorts",
            "Light jacket",
            "Comfortable walking shoes",
            "Sneakers"
        ])

    # Add activity-specific items
    activity_items = {
        "hiking": ["Hiking boots", "Backpack", "Water bottle", "Trail snacks"],
        "beach": ["Swimsuit", "Beach towel", "Snorkel gear", "Waterproof bag"],
        "formal": ["Dress clothes", "Dress shoes", "Nice accessories"],
        "adventure": ["Athletic wear", "Action camera", "First aid kit"],
        "business": ["Business attire", "Laptop", "Business cards", "Portfolio"]
    }

    for activity in trip_activities:
        activity_lower = activity.lower()
        for key, items in activity_items.items():
            if key in activity_lower:
                checklist["activities"].extend(items)

    # Remove duplicates
    for category in checklist:
        checklist[category] = list(set(checklist[category]))

    return checklist


def generate_pre_trip_checklist(destination_country: str, departure_date: str) -> List[Dict[str, Any]]:
    """
    Generate pre-trip preparation checklist with timeline.
    """
    try:
        departure = datetime.fromisoformat(departure_date)
    except:
        # If date parsing fails, use relative timeline
        departure = datetime.now() + timedelta(days=30)

    today = datetime.now()
    days_until = (departure - today).days

    checklist = []

    # 3 months before (90 days)
    if days_until >= 90:
        checklist.append({
            "timeline": "3 months before",
            "tasks": [
                "Research destination and create wish list",
                "Check passport expiration (needs 6+ months validity)",
                "Research visa requirements",
                "Set up travel alerts for flights",
                "Start saving/budgeting for trip"
            ]
        })

    # 2 months before (60 days)
    if days_until >= 60:
        checklist.append({
            "timeline": "2 months before",
            "tasks": [
                "Book flights",
                "Book accommodation",
                "Apply for visa if needed",
                "Purchase travel insurance",
                "Check vaccination requirements",
                "Research local customs and etiquette"
            ]
        })

    # 1 month before (30 days)
    if days_until >= 30:
        checklist.append({
            "timeline": "1 month before",
            "tasks": [
                "Book major activities and tours",
                "Notify bank of travel dates",
                "Set up international phone plan",
                "Make restaurant reservations",
                "Check weather forecasts",
                "Start gathering packing items"
            ]
        })

    # 2 weeks before
    if days_until >= 14:
        checklist.append({
            "timeline": "2 weeks before",
            "tasks": [
                "Confirm all reservations",
                "Print important documents",
                "Exchange some currency",
                "Refill prescriptions",
                "Arrange pet/plant care",
                "Hold mail delivery"
            ]
        })

    # 1 week before
    if days_until >= 7:
        checklist.append({
            "timeline": "1 week before",
            "tasks": [
                "Check in for flights",
                "Download offline maps",
                "Pack luggage",
                "Charge all devices",
                "Clean out refrigerator",
                "Set up home security"
            ]
        })

    # Day before
    checklist.append({
        "timeline": "Day before departure",
        "tasks": [
            "Re-check flight times",
            "Prepare carry-on essentials",
            "Take out trash",
            "Check weather at destination",
            "Get good rest",
            "Set multiple alarms"
        ]
    })

    return checklist


def generate_trip_plan(trip_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate complete trip plan with all components.
    """
    destination = trip_data.get("destination", {})
    duration = trip_data.get("duration_days", 7)
    budget = trip_data.get("budget", {}).get("total", 0)
    departure_date = trip_data.get("departure_date", "")

    # Get user preferences
    prefs = get_preferences()
    interests = prefs.get("interests", [])
    pace = prefs.get("pace_preference", "moderate")
    accommodation_level = prefs.get("budget_level", "mid-range")

    # Generate components
    plan = {
        "trip_id": trip_data.get("id", ""),
        "destination": destination,
        "dates": {
            "departure": trip_data.get("departure_date", ""),
            "return": trip_data.get("return_date", ""),
            "duration_days": duration
        },
        "itinerary": generate_daily_itinerary(
            destination.get("city", ""),
            duration,
            interests,
            pace
        ),
        "budget": calculate_budget_breakdown(budget, duration, accommodation_level),
        "packing_checklist": generate_packing_checklist(
            trip_data.get("climate", "moderate"),
            duration,
            trip_data.get("activities", [])
        ),
        "pre_trip_checklist": generate_pre_trip_checklist(
            destination.get("country", ""),
            departure_date
        ),
        "generated_at": datetime.now().isoformat()
    }

    return plan


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate travel plan')
    parser.add_argument('--trip-id', help='Trip ID from database')
    parser.add_argument('--output', help='Output JSON file path')

    args = parser.parse_args()

    if not args.trip_id:
        print("Error: --trip-id required")
        sys.exit(1)

    from travel_db import get_trip_by_id

    trip = get_trip_by_id(args.trip_id)
    if not trip:
        print(f"Error: Trip {args.trip_id} not found")
        sys.exit(1)

    plan = generate_trip_plan(trip)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(plan, f, indent=2)
        print(f"✓ Travel plan generated: {args.output}")
    else:
        print(json.dumps(plan, indent=2))
