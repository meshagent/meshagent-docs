import asyncio
from typing import Literal

from meshagent.api import TOOL_SEARCH_ANNOTATION
from meshagent.api.services import ServiceHost
from meshagent.otel import otel_config
from meshagent.tools import FunctionTool, Toolkit, ToolContext

otel_config(service_name="room_tool_search_menu")
service = ServiceHost()


MENU = {
    "vegetarian": {
        "name": "Roasted vegetable grain bowls",
        "description": "Quinoa, roasted seasonal vegetables, chickpeas, feta, and lemon tahini.",
        "price_per_person": 16,
    },
    "vegan": {
        "name": "Coconut curry tofu boxes",
        "description": "Crispy tofu, coconut curry vegetables, jasmine rice, and cucumber salad.",
        "price_per_person": 18,
    },
    "gluten_free": {
        "name": "Citrus chicken salad plates",
        "description": "Grilled chicken, greens, avocado, citrus vinaigrette, and roasted potatoes.",
        "price_per_person": 19,
    },
    "standard": {
        "name": "Mediterranean lunch spread",
        "description": "Chicken skewers, falafel, hummus, tabbouleh, pita, and chopped salad.",
        "price_per_person": 17,
    },
}


DietaryStyle = Literal["vegetarian", "vegan", "gluten_free", "standard"]


class RecommendLunch(FunctionTool):
    def __init__(self):
        super().__init__(
            name="recommend_lunch",
            title="Recommend lunch",
            description=(
                "Recommend a lunch menu for a team based on dietary style. "
                "Use this when someone asks for catering, meals, office lunch, "
                "or menu ideas."
            ),
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["dietary_style", "guests"],
                "properties": {
                    "dietary_style": {
                        "type": "string",
                        "enum": ["vegetarian", "vegan", "gluten_free", "standard"],
                        "description": "The primary dietary requirement for the group.",
                    },
                    "guests": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Number of people eating lunch.",
                    },
                },
            },
        )

    async def execute(
        self, context: ToolContext, *, dietary_style: DietaryStyle, guests: int
    ):
        del context
        menu = MENU[dietary_style]
        subtotal = guests * menu["price_per_person"]
        return {
            "recommendation": menu["name"],
            "description": menu["description"],
            "guests": guests,
            "price_per_person": menu["price_per_person"],
            "subtotal": subtotal,
        }


class CalculateCateringQuote(FunctionTool):
    def __init__(self):
        super().__init__(
            name="calculate_catering_quote",
            title="Calculate catering quote",
            description=(
                "Calculate a catering quote for a team lunch. Use this after "
                "choosing a menu item or when someone asks for a meal budget."
            ),
            input_schema={
                "type": "object",
                "additionalProperties": False,
                "required": ["dietary_style", "guests", "include_drinks"],
                "properties": {
                    "dietary_style": {
                        "type": "string",
                        "enum": ["vegetarian", "vegan", "gluten_free", "standard"],
                        "description": "The primary dietary requirement for the group.",
                    },
                    "guests": {
                        "type": "integer",
                        "minimum": 1,
                        "description": "Number of people eating lunch.",
                    },
                    "include_drinks": {
                        "type": "boolean",
                        "description": "Whether to include bottled drinks at $3 per person.",
                    },
                },
            },
        )

    async def execute(
        self,
        context: ToolContext,
        *,
        dietary_style: DietaryStyle,
        guests: int,
        include_drinks: bool,
    ):
        del context
        menu = MENU[dietary_style]
        food_total = guests * menu["price_per_person"]
        drinks_total = guests * 3 if include_drinks else 0
        service_fee = round((food_total + drinks_total) * 0.12, 2)
        total = round(food_total + drinks_total + service_fee, 2)
        return {
            "menu": menu["name"],
            "guests": guests,
            "food_total": food_total,
            "drinks_total": drinks_total,
            "service_fee": service_fee,
            "total": total,
        }


@service.path(path="/menu", identity="menu-toolkit")
class MenuToolkit(Toolkit):
    def __init__(self):
        super().__init__(
            name="menu-toolkit",
            title="Menu toolkit",
            description=(
                "Searchable catering and lunch-planning tools for menu "
                "recommendations, dietary needs, and team meal quotes."
            ),
            annotations={TOOL_SEARCH_ANNOTATION: "true"},
            tools=[RecommendLunch(), CalculateCateringQuote()],
        )


if __name__ == "__main__":
    print(f"running menu toolkit on port {service.port}")
    asyncio.run(service.run())
