"""API layer"""

# 3rd party
from fastapi import APIRouter

# local
from .auth.router import router as auth_router
from .game.router import router as game_router


router = APIRouter()
"""Main router"""

router.include_router(auth_router)
router.include_router(game_router)
