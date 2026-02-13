# """
# FastAPI Workers and Background Tasks Configuration
# """
# from typing import Callable
# from fastapi import FastAPI
# import asyncio


# class BackgroundTaskManager:
#     """Manage background tasks and workers"""

#     tasks: list[Callable] = []

#     @classmethod
#     def register(cls, task: Callable) -> Callable:
#         """Register a background task"""
#         cls.tasks.append(task)
#         return task

#     @classmethod
#     async def start_all(cls):
#         """Start all registered background tasks"""
#         await asyncio.gather(*[task() for task in cls.tasks])


# # Example background tasks (uncomment to use)
# # @BackgroundTaskManager.register
# # async def example_background_task():
# #     """Example background task"""
# #     while True:
# #         print("Running background task...")
# #         await asyncio.sleep(60)
