from OpenGL.GL import *
from core import OpenGLUtils
from material import Material

#This material demonstrates specular lighting
class SpecularMaterial(Material):
	def __init__(self):
		#Code for the vertex shader
		vsCode = """
		// required ins, outs and uniforms for 
		in vec3 vertexPosition;
        in vec2 vertexUV;
        in vec3 vertexNormal;
        in vec3 vertexColor;
        
        out vec3 position;
        out vec2 UV;
        out vec3 normal; 
        out vec3 vColor;
        
        uniform mat4 projectionMatrix;
        uniform mat4 viewMatrix;
        uniform mat4 modelMatrix;
		
		
        uniform bool useFog;
        out float cameraDistance; 
		
        // not going to work with shadows right now
        //uniform bool receiveShadow;
        
        // assume that at most one light casts shadows
        //   and its values have been passed in here
        uniform mat4 shadowProjectionMatrix;
        uniform mat4 shadowViewMatrix;
        out vec4 positionFromShadowLight;
		
		void main(){
			// out values being sent to fragment shader
            position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            UV = vertexUV;
            normal = normalize(mat3(modelMatrix) * vertexNormal); // normalize in case of model scaling
            vColor = vertexColor;
			
			
			gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
		}
		"""
		
		vsCode = """
		in vec3 vertexPosition;
		in vec3 vertexUV;
		
		out vec3 position;
		uniform mat4 projectionMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 modelMatrix;
		
		void main(){
			position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
		}
		"""
		
		fsCode = """
        in vec3 position;
        in vec2 UV;
        in vec3 normal;
        
        uniform bool useVertexColors;
        in vec3 vColor;
        
        uniform bool useTexture;
        uniform sampler2D image;
        
        uniform float alphaTest;
        
        uniform bool useLight;
        
        struct Light
        {
            bool isAmbient;
            bool isDirectional;
            bool isPoint;
            
            // used by all lights
            float strength;
            vec3 color;
            
            // used by point light
            vec3 position;

            // used by directional light
            vec3 direction;
        };
		
		void main(){
		
		}
		"""
		
		fsCode = """
		in vec3 position;
		
		void main(){
			vec3 lightColor = vec3(0.0,0.0,1.0);
			float ambientStrength = 0.2;
			vec3 ambient = ambientStrength * lightColor;
			
			vec3 objectColor = vec3(1.0,1.0,1.0);
			vec3 result = ambient * objectColor;
			gl_FragColor = vec4(result, 1.0);
		}
		"""
		
		# initialize shaders
		super().__init__(vsCode, fsCode)
		
		# set default render values
		self.drawStyle = GL_TRIANGLES
		
		