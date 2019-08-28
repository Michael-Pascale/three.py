from lights import Light

class PointLight(Light):

    # TODO: add attenuation coefficients (constant, linear, quadratic)
    def __init__(self, position=[0,0,0], color=[1,1,1], strength=1, isSpecular=0):
        super().__init__(position=position, color=color, strength=strength)

        self.uniformList.setUniformValue("isPoint", 1)
        self.uniformList.setUniformValue("isSpecular",isSpecular)
