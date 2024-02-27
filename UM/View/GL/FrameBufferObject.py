# Copyright (c) 2018 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

from PyQt5.QtGui import QImage, QOpenGLFramebufferObject, QOpenGLFramebufferObjectFormat


class FrameBufferObject:
    """An interface for OpenGL FrameBuffer Objects.

    This class describes a minimal interface that is expected of FrameBuffer Object
    classes.
    """
    def __init__(self, width: int, height: int, samples: int) -> None:
        super().__init__()

        buffer_format = QOpenGLFramebufferObjectFormat()
        buffer_format.setAttachment(QOpenGLFramebufferObject.Depth)
        self._fbo = QOpenGLFramebufferObject(width, height, buffer_format)
        self._contents = None
        self._fbo2 = None
        self._usingAA = False
        if samples > 0:
            buffer_format = QOpenGLFramebufferObjectFormat()
            buffer_format.setAttachment(QOpenGLFramebufferObject.Depth)
            buffer_format.setSamples(samples)
            self._fbo2 = QOpenGLFramebufferObject(width, height, buffer_format)
            if self._fbo2.format().samples() > 0:
                self._usingAA = True
            else:
                self._fbo2 = None

    def _AAEnabled(self) -> bool:
        return self._fbo2 is not None and self._usingAA

    def getUsingAA(self) -> bool:
        return self._AAEnabled()

    def setUsingAA(self, usingAA: bool) -> None:
        self._usingAA = usingAA

    def getSamples(self) -> int:
        if self._fbo2 is not None:
            return self._fbo2.format().samples()
        return 0

    def getTextureId(self) -> int:
        """Get the texture ID of the texture target of this FBO."""
        if self._AAEnabled():
            QOpenGLFramebufferObject.blitFramebuffer(self._fbo, self._fbo2)
        return self._fbo.texture()

    def bind(self) -> None:
        """Bind the FBO so it can be rendered to."""
        self._contents = None
        if self._AAEnabled():
            self._fbo2.bind()
        else:
            self._fbo.bind()

    def release(self) -> None:
        """Release the FBO so it will no longer be rendered to."""
        if self._AAEnabled():
            self._fbo2.release()
        else:
            self._fbo.release()

    def getContents(self) -> QImage:
        """Get the contents of the FBO as an image data object."""
        if not self._contents:
            self._contents = self._fbo.toImage()

        return self._contents