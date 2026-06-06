from datetime import datetime

from google.adk.tools.tool_context import ToolContext
from google.genai import types

IMAGEN_MODEL = "imagen-4.0-generate-001"
GEMINI_IMAGE_MODEL = "gemini-2.5-flash-image"


async def generate_campaign_thumbnail(prompt: str, tool_context: ToolContext):
    """Generates a campaign thumbnail image and saves it as a session artifact.

    Args:
        prompt: Detailed visual description for the thumbnail (style, colors,
            composition, text overlays, mood).

    Returns:
        A dict with status, filename, and any error details.
    """
    from google.genai import Client

    client = Client()
    image_bytes = _generate_with_imagen(client, prompt)
    if image_bytes is None:
        image_bytes = _generate_with_gemini_image(client, prompt)
    if image_bytes is None:
        return {
            "status": "failed",
            "detail": (
                "Image generation failed. Ensure your Google API key has image "
                "generation enabled (paid plan may be required for Imagen)."
            ),
        }

    filename = f"campaign_thumbnail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    await tool_context.save_artifact(
        filename,
        types.Part.from_bytes(data=image_bytes, mime_type="image/png"),
    )
    return {
        "status": "success",
        "detail": "Campaign thumbnail generated and saved to artifacts.",
        "filename": filename,
    }


def _generate_with_imagen(client, prompt: str) -> bytes | None:
    try:
        response = client.models.generate_images(
            model=IMAGEN_MODEL,
            prompt=prompt,
            config={"number_of_images": 1, "aspect_ratio": "16:9"},
        )
    except Exception:
        return None

    if not response.generated_images:
        return None

    image = response.generated_images[0].image
    return image.image_bytes if image else None


def _generate_with_gemini_image(client, prompt: str) -> bytes | None:
    try:
        response = client.models.generate_content(
            model=GEMINI_IMAGE_MODEL,
            contents=f"Generate a marketing campaign thumbnail image: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )
    except Exception:
        return None

    if not response.candidates:
        return None

    for part in response.candidates[0].content.parts:
        inline_data = getattr(part, "inline_data", None)
        if inline_data and inline_data.data:
            return inline_data.data

    return None
