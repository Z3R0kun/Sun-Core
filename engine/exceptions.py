class AnimationIDNotFound(Exception):
    "This exceptions is called when you tried to use an animation id that doesn't exists"
    pass
class ParticleShapeNotFound(Exception):
    "This exceptions is called when you tried to make a particle with a non-defined shape"
    pass
class NotSupportedTextCharacter(Exception):
    "This exceptions is called when you tried to use text charatcer not available"
    pass
