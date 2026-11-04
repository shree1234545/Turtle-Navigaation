
import json
import math

# Reference coordinates for 10 shapes
references = {
    "square": [(2,2),(8,2),(8,8),(2,8),(2,2)],
    "triangle": [(5,8),(8,2),(2,2),(5,8)],
    "rectangle": [(2,3),(8,3),(8,7),(2,7),(2,3)],
    "diamond": [(5,8),(8,5),(5,2),(2,5),(5,8)],
    "pentagon": [(5,8),(8,6),(7,2),(3,2),(2,6),(5,8)],
    "house": [(2,2),(2,6),(5,9),(8,6),(8,2),(2,2)],
    "arrow": [(2,5),(7,5),(7,8),(10,5),(7,2),(7,5)],
    "a": [(2,2),(5,8),(8,2),(3,5),(7,5)],
    "t": [(2,8),(8,8),(5,8),(5,2)],
    "star": [(5,9),(6,6),(9,6),(7,4),(8,1),
             (5,3),(2,1),(3,4),(1,6),(4,6),(5,9)]
}

def chamfer(a, b):
    def directed(p, q):
        return sum(
            min(math.dist(x, y) for y in q)
            for x in p
        ) / len(p)

    return (directed(a, b) + directed(b, a)) / 2

with open("d3_results.json") as f:
    results = json.load(f)

print("\nD6: AI DRAWING EVALUATION")
print("-" * 55)

scores = []

for item in results:
    prompt = item["prompt"].lower()
    data = item.get("output")

    # Find the corresponding reference shape
    name = next(
        (n for n in references if n in prompt),
        None
    )

    if not name or not isinstance(data, dict):
        print(f"{item['prompt']}: No result to evaluate")
        continue

    points = data.get("points", [])

    if not isinstance(points, list) or not points:
        print(f"{item['prompt']}: Invalid points")
        continue

    try:
        generated = [
            (float(p[0]), float(p[1]))
            for p in points
            if isinstance(p, list) and len(p) == 2
        ]

        if len(generated) != len(points):
            raise ValueError("Invalid point format")

        if not all(
            math.isfinite(x) and math.isfinite(y)
            for x, y in generated
        ):
            raise ValueError("Non-finite coordinates")

        distance = chamfer(generated, references[name])
        score = 100 / (1 + distance)

        scores.append(score)
        print(
            f"{item['prompt']}: "
            f"Distance = {distance:.2f}, "
            f"Score = {score:.2f}/100"
        )

    except (TypeError, ValueError, IndexError):
        print(f"{item['prompt']}: Invalid coordinates")

if scores:
    print("-" * 55)
    print(f"Average score: {sum(scores)/len(scores):.2f}/100")
    print(f"Shapes evaluated: {len(scores)}")
else:
    print("No shapes could be evaluated.")
