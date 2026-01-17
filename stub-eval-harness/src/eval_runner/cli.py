import json
import typer

app = typer.Typer(no_args_is_help=True)

@app.command()
def eval_run(
    config: str = typer.Option(..., "--config", help="Path to config file"),
):
    """Run evaluation with the given config file."""
    print(f"Running eval with config: {config}")
    # read in file from data/prompts.jsonl its a id, prompt pair
    with open("data/prompts.jsonl", "r") as f:
        prompts = [json.loads(line) for line in f]
    
    output_dict = {}
    for prompt in prompts:
        response = dummyAIPass(prompt)
        output_dict[prompt["id"]] = response

    # write to file in outputs/results.jsonl
    with open("outputs/results.jsonl", "w") as f:
        for id, response in output_dict.items():
            f.write(json.dumps({"id": id, "response": response}) + "\n")

# Just sends req and return
def dummyAIPass(prompt_object: dict):
    # dummy response for id #
    response = "dummy response for prompt with id: " + prompt_object["id"]

    return response
