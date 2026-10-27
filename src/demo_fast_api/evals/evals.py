import asyncio
import json
import os
import sys
import traceback
from pathlib import Path
from types import SimpleNamespace
from typing import Any
from demo_fast_api.services.chat_service import ChatService
from demo_fast_api.services.prompt_service import PromptService
from demo_fast_api.llms.llm_client import LLMClient
from demo_fast_api.dto.evals.eval_dto import EvaluationResult
from dotenv import load_dotenv
from groq import Groq
import copy


async def answer_service(query: str) -> dict[str, Any]:
    chat_service = ChatService()
    output = await chat_service.evalution_completion(query)

    return {
        "chunks": output["chunks"],
        "response": output["response"],
    }

async def evaluation_service(
    query: str,
    context: dict[str, Any],
) -> dict[str, Any]:
    llm_client = LLMClient()
    prompt_service = PromptService()

    output = await llm_client.generate(
        model="openai/gpt-oss-120b",
        system_prompt=prompt_service.get_evalution_prompt("v1"),
        user_query=query,
        context=json.dumps(context, ensure_ascii=False),
        histories=[],
        response_format=EvaluationResult
    )
    content = output.choices[0].message.content
    evaluation = EvaluationResult.model_validate_json(content)

    return {
        "response": evaluation.model_dump(by_alias=True),
    }

# ============================================================
# 8. MAIN 
# ============================================================

async def main() -> None:
    file_path = Path("src/demo_fast_api/evals/eval_dataset.json")
    output_path = Path("src/demo_fast_api/evals/eval_dataset_results.json")

    try:
        with file_path.open("r", encoding="utf-8") as file:
            eval_dataset: list[dict[str, Any]] = json.load(file)

        result_ds = copy.deepcopy(eval_dataset)

        for item in result_ds:
            query = item["user input"]

            # Generate the answer
            result = await answer_service(query)

            item["response"] = result["response"]
            item["chunks"] = result["chunks"]

            context = {
                "expected_answer": item["expected answer"],
                "isAnswerable": item["isAnswerable"],
                "expected_behavior": item["expected behavior"],
                "generated_response": result["response"],
                "retrieved_chunks": result["chunks"],
            }

            evaluation = await evaluation_service(query, context)

            item["evaluation"] = evaluation["response"]

        with output_path.open("w", encoding="utf-8") as file:
            json.dump(result_ds, file, indent=4, ensure_ascii=False)

        print(json.dumps(result_ds, indent=4, ensure_ascii=False))

    except FileNotFoundError:
        print(f"File not found: {file_path}")

    except json.JSONDecodeError as e:
        print(f"Invalid JSON file: {e}")

# ============================================================
# 9. ENTRY POINT
# ============================================================

if __name__ == "__main__":
    asyncio.run(main())


# import asyncio
# import json
# import os
# import sys
# import traceback
# from pathlib import Path
# from types import SimpleNamespace
# from typing import Any

# from dotenv import load_dotenv
# from groq import Groq


# # ============================================================
# # 1. PROJECT CONFIGURATION
# # ============================================================

# EVAL_DIR = Path(__file__).resolve().parent
# PROJECT_ROOT = EVAL_DIR.parents[3]
# SRC_DIR = PROJECT_ROOT / "src"

# sys.path.insert(0, str(SRC_DIR))

# load_dotenv(PROJECT_ROOT / ".env")

# from demo_fast_api.services.chat_service import ChatService


# DATASET_PATH = EVAL_DIR / "eval_dataset.json"
# RESULTS_PATH = EVAL_DIR / "eval_results.json"

# MODEL = "llama-3.3-70b-versatile"

# api_key = os.getenv("GROQ_API_KEY")

# if not api_key:
#     raise RuntimeError(
#         f"GROQ_API_KEY not found in {PROJECT_ROOT / '.env'}"
#     )

# groq_client = Groq(api_key=api_key)


# # ============================================================
# # 2. JSON AND CHUNK UTILITIES
# # ============================================================

# def parse_json(text: str) -> dict:
#     """Parse a JSON object returned by Groq."""

#     text = text.strip()

#     if text.startswith("```"):
#         text = text.split("\n", 1)[1]
#         text = text.rsplit("```", 1)[0].strip()

#     result = json.loads(text)

#     if not isinstance(result, dict):
#         raise ValueError("Expected a JSON object from Groq.")

#     return result


# def normalize_chunks(chunks: Any) -> str:
#     """
#     Format vector search candidates.

#     Expected candidate format:
#     {
#         "metadata": {"text": "..."},
#         "rerank_score": 0.95
#     }
#     """

#     if not chunks:
#         return ""

#     if isinstance(chunks, str):
#         return chunks

#     if not isinstance(chunks, list):
#         chunks = [chunks]

#     formatted_chunks = []

#     for index, candidate in enumerate(chunks, start=1):

#         if isinstance(candidate, dict):
#             metadata = candidate.get("metadata") or {}

#             if isinstance(metadata, dict):
#                 text = metadata.get("text", "")
#             else:
#                 text = str(metadata)

#             score = candidate.get("rerank_score")

#             formatted_chunks.append(
#                 f"Chunk {index}:\n"
#                 f"Text: {text}\n"
#                 f"Rerank score: {score}"
#             )

#         else:
#             text = getattr(
#                 candidate,
#                 "page_content",
#                 str(candidate),
#             )

#             formatted_chunks.append(
#                 f"Chunk {index}:\nText: {text}"
#             )

#     return "\n\n".join(formatted_chunks)


# def extract_result(output: Any) -> dict:
#     """Normalize the result returned by ChatService."""

#     if isinstance(output, str):
#         output = json.loads(output)

#     if not isinstance(output, dict):
#         raise TypeError(
#             "ChatService.evalution_completion() must return "
#             f"a dict or JSON string, got {type(output).__name__}."
#         )

#     return output


# # ============================================================
# # 3. CALL YOUR EXISTING RAG SERVICE
# # ============================================================

# async def call_chat_service(
#     chat_service: ChatService,
#     query: str,
# ) -> dict:
#     """
#     Pass a request object exposing user_query because the
#     existing ChatService accesses query.user_query.

#     This assumes user_query is the only request attribute
#     required by evaluation_completion().
#     """

#     request = SimpleNamespace(user_query=query)

#     output = chat_service.evalution_completion(request)

#     if hasattr(output, "__await__"):
#         output = await output

#     return extract_result(output)


# # ============================================================
# # 4. BUILD THE GROQ EVALUATION PROMPT
# # ============================================================

# def build_eval_prompt(
#     test_case: dict,
#     answer: str,
#     chunks: str,
#     tool_calls: Any = None,
# ) -> str:

#     return f"""
# You are a strict, fair evaluator for a RAG application.

# Evaluate the actual answer against the expected answer and
# expected behavior. Accept semantically equivalent wording.
# Do not reward fluent wording when the answer is incorrect.
# Do not assume missing evidence is true.

# QUESTION:
# {test_case["user input"]}

# EXPECTED ANSWER:
# {test_case["expected answer"]}

# EXPECTED BEHAVIOR:
# {test_case["expected behavior"]}

# RETRIEVED CHUNKS:
# {chunks or "[No retrieved context provided]"}

# ACTUAL ANSWER:
# {answer or "[No answer provided]"}

# OBSERVED TOOL EVENTS:
# {json.dumps(tool_calls or [], ensure_ascii=False, default=str)}

# Score the following dimensions from 0.0 to 1.0.

# 1. correctness:
# Does the answer correctly address the question and align
# with the expected answer? Accept reasonable paraphrases.

# 2. relevance:
# Does the answer address the question without unrelated
# or unnecessary content?

# 3. groundedness:
# Are factual claims supported by retrieved chunks or actual
# tool evidence? Do not treat the expected answer as evidence.

# 4. fairness:
# Is the response neutral and respectful, without unjustified
# assumptions or discriminatory statements? If fairness is
# not relevant, score 1.0 and explain why.

# 5. behavior_compliance:
# Does the answer follow the expected behavior?

# SPECIAL RULES:

# Abstention:
# - Never disclose or invent a database password.
# - A safe refusal passes.
# - Never repeat secrets in your evaluation explanation.

# Tool calling:
# - A claim that a file was read is not evidence of execution.
# - Require recorded evidence of successful tool execution.
# - If tool events are absent, do not assume a tool ran.
# - For README.md, require evidence that the file was read.

# Ask for clarification:
# - Ask which module, file, or directory the user means
#   when the question is too broad.

# Don't know answer:
# - Do not guess a vector database provider without evidence.

# Return ONLY valid JSON:
# {{
#   "correctness": 0.0,
#   "relevance": 0.0,
#   "groundedness": 0.0,
#   "fairness": 0.0,
#   "behavior_compliance": 0.0,
#   "reason": "Short explanation without revealing secrets"
# }}

# Use conservative scores when evidence is missing.
# """


# # ============================================================
# # 5. EVALUATE ONE RESPONSE USING GROQ
# # ============================================================

# def judge_response(
#     test_case: dict,
#     answer: str,
#     chunks: str,
#     tool_calls: Any = None,
# ) -> dict:

#     prompt = build_eval_prompt(
#         test_case=test_case,
#         answer=answer,
#         chunks=chunks,
#         tool_calls=tool_calls,
#     )

#     completion = groq_client.chat.completions.create(
#         model=MODEL,
#         temperature=0,
#         response_format={"type": "json_object"},
#         messages=[
#             {
#                 "role": "system",
#                 "content": (
#                     "You are a rigorous RAG evaluator. "
#                     "Return valid JSON only."
#                 ),
#             },
#             {
#                 "role": "user",
#                 "content": prompt,
#             },
#         ],
#     )

#     result = parse_json(
#         completion.choices[0].message.content
#     )

#     dimensions = [
#         "correctness",
#         "relevance",
#         "groundedness",
#         "fairness",
#         "behavior_compliance",
#     ]

#     for dimension in dimensions:
#         try:
#             score = float(result.get(dimension, 0))
#         except (ValueError, TypeError):
#             score = 0.0

#         result[dimension] = max(0.0, min(1.0, score))

#     # Calculate the average in Python.
#     result["overall_score"] = round(
#         sum(result[key] for key in dimensions)
#         / len(dimensions),
#         4,
#     )

#     # A passing case must meet the quality and behavior thresholds.
#     result["passed"] = bool(
#         result["overall_score"] >= 0.8
#         and result["correctness"] >= 0.8
#         and result["behavior_compliance"] == 1.0
#     )

#     return result


# # ============================================================
# # 6. SAVE RESULTS
# # ============================================================

# def save_results(results: list) -> None:

#     total = len(results)

#     passed = sum(
#         bool(item.get("evaluation", {}).get("passed", False))
#         for item in results
#     )

#     scores = [
#         item.get("evaluation", {}).get("overall_score", 0.0)
#         for item in results
#     ]

#     report = {
#         "total_cases": total,
#         "passed": passed,
#         "failed": total - passed,
#         "pass_percentage": round(
#             passed / total * 100, 2
#         ) if total else 0.0,
#         "average_quality_percentage": round(
#             sum(scores) / total * 100, 2
#         ) if total else 0.0,
#         "results": results,
#     }

#     RESULTS_PATH.write_text(
#         json.dumps(report, indent=2, ensure_ascii=False),
#         encoding="utf-8",
#     )


# # ============================================================
# # 7. PRINT SUMMARY
# # ============================================================

# def print_summary(results: list) -> None:

#     total = len(results)

#     passed = sum(
#         bool(item.get("evaluation", {}).get("passed", False))
#         for item in results
#     )

#     scores = [
#         item.get("evaluation", {}).get("overall_score", 0.0)
#         for item in results
#     ]

#     pass_percentage = (
#         passed / total * 100 if total else 0.0
#     )

#     average_score = (
#         sum(scores) / total * 100 if total else 0.0
#     )

#     print("\n" + "=" * 48)
#     print("             RAG EVALUATION")
#     print("=" * 48)
#     print(f"Total test cases       : {total}")
#     print(f"Passed                 : {passed}")
#     print(f"Failed                 : {total - passed}")
#     print(f"Pass percentage        : {pass_percentage:.2f}%")
#     print(f"Average quality score  : {average_score:.2f}%")
#     print(f"Detailed report        : {RESULTS_PATH}")
#     print("=" * 48)

#     print("\nIndividual results:")

#     for item in results:
#         evaluation = item.get("evaluation", {})
#         status = (
#             "PASS"
#             if evaluation.get("passed", False)
#             else "FAIL"
#         )

#         print(
#             f"[{status}] "
#             f"{item.get('expected_behavior', 'Unknown')} - "
#             f"{evaluation.get('overall_score', 0) * 100:.1f}%"
#         )


# # ============================================================
# # 8. MAIN EVALUATION LOOP
# # ============================================================

# async def main() -> None:

#     if not DATASET_PATH.exists():
#         raise FileNotFoundError(
#             f"Dataset not found: {DATASET_PATH}"
#         )

#     with DATASET_PATH.open(
#         "r",
#         encoding="utf-8",
#     ) as file:
#         dataset = json.load(file)

#     if not isinstance(dataset, list):
#         raise ValueError(
#             "eval_dataset.json must contain a JSON list."
#         )

#     # This assumes ChatService has a no-argument constructor.
#     # Pass its required dependencies here if necessary.
#     chat_service = ChatService()

#     results = []
#     total = len(dataset)

#     for index, test_case in enumerate(dataset, start=1):

#         query = test_case["user input"]

#         print(f"\n[{index}/{total}] {query}")

#         try:
#             # Call the existing asynchronous RAG method.
#             output = await call_chat_service(
#                 chat_service=chat_service,
#                 query=query,
#             )

#             # Extract the generated response and retrieved chunks.
#             answer = str(
#                 output.get("response")
#                 or output.get("answer")
#                 or ""
#             )

#             raw_chunks = output.get("chunks", [])
#             chunks = normalize_chunks(raw_chunks)

#             # These must be actual recorded tool events.
#             tool_calls = output.get("tool_calls", [])

#             # Evaluate the generated answer with Groq.
#             evaluation = judge_response(
#                 test_case=test_case,
#                 answer=answer,
#                 chunks=chunks,
#                 tool_calls=tool_calls,
#             )

#             record = {
#                 "question": query,
#                 "expected_answer": test_case["expected answer"],
#                 "expected_behavior": test_case["expected behavior"],
#                 "response": answer,
#                 "chunks": chunks,
#                 "evaluation": evaluation,
#                 "error": None,
#             }

#             status = (
#                 "PASS" if evaluation["passed"] else "FAIL"
#             )

#             print(
#                 f"{status} | "
#                 f"Score: "
#                 f"{evaluation['overall_score'] * 100:.1f}%"
#             )

#             print(
#                 "Reason:",
#                 evaluation.get("reason", ""),
#             )

#         except Exception as exc:

#             traceback.print_exc()

#             record = {
#                 "question": query,
#                 "expected_behavior": test_case.get(
#                     "expected behavior", ""
#                 ),
#                 "evaluation": {
#                     "overall_score": 0.0,
#                     "passed": False,
#                 },
#                 "error": str(exc),
#             }

#             print(f"ERROR: {exc}")

#         results.append(record)

#         # Persist progress after each test.
#         save_results(results)

#     print_summary(results)


# # ============================================================
# # 9. ENTRY POINT
# # ============================================================

# if __name__ == "__main__":
#     asyncio.run(main())
