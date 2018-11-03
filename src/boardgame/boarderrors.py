class BoardError(BaseException):
	pass

class SquareNotEmpty(BoardError):
	pass

class NoMoveError(BoardError):
	pass

class MovementAllowanceExceeded(BoardError):
	pass

class MoveFailedError(BoardError):
	pass

class PieceNotFoundError(BoardError):
	pass

class MultipleRenderersError(BoardError):
	pass

class GameCommandFormatException(BoardError):
	pass

class InvalidData(BoardError):
	pass
