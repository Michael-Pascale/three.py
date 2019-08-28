from OpenGL.GL import *
from core import OpenGLUtils
from material import Material

#This material demonstrates specular lighting
#tutorial found online courtesy (https://learnopengl.com/Lighting/Basic-Lighting)
class SpecularMaterial(Material):
	def __init__(self):
		#Code for the vertex shader
		
		#These shaders hope to improve on the basic specular light by using the light struct and built in lights from three py
		#rather than simple uniforms only
		
		vsCode = """
		in vec3 vertexPosition;
		in vec3 vertexUV;
		in vec3 vertexNormal;
		
		out vec3 position;
		out vec3 Normal;
		uniform mat4 projectionMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 modelMatrix;
		
		out vec3 FragPos;
		
		void main(){
			position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
			//Normal = vertexNormal;
			//This line seems inefficient
			Normal = mat3(transpose(inverse(modelMatrix))) * vertexNormal;
			FragPos = vec3(modelMatrix * vec4(vertexPosition, 1));
		}
		"""
		
		#code for the fragment shader
		fsCode = """
		in vec3 position;
		in vec3 Normal;
		in vec3 FragPos;
		
		uniform vec3 viewPos;
		uniform vec3 viewDir;
		//uniform vec3 lightPosition;
		
		//struct for the light objects
		struct Light{
			bool isAmbient;
			bool isDirectional;
			bool isPoint;
			bool isSpecular;//should be mutually exclusive with isAmbient
			
			//used by all lights
			float strength;
			vec3 color;
			
			//used by point lights only
			vec3 position;
			
			//used by directional lights only
			vec3 direction;
		};
		
		uniform Light light0;//using nomenclature of three py for the lights
		
		void main(){
			//TODO: move declared variables to uniforms when convenient/needed
			
			//ambient light
			//vec3 lightPosition = vec3(0.0,3.0,4.0);
			vec3 lightColor = vec3(1.0,1.0,1.0);
			float ambientStrength = 0.2;
			vec3 ambient = ambientStrength * lightColor;
			
			//point light(currently only 1)(diffuse)
			float diffuseStrength = 0.5;
			vec3 norm = normalize(Normal);
			vec3 lightDir = normalize(light0.position - FragPos);
			float diff = max(dot(norm, lightDir), 0.0);
			vec3 diffuse = diff * lightColor * diffuseStrength;
			
			//specular light
			vec3 specular;
			if(light0.isSpecular){
				float specularStrength = 0.7;
				//vec3 viewDir = normalize(viewPos - FragPos);
				vec3 reflectDir = reflect(-lightDir, norm);
				float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16);
				specular = specularStrength * spec * lightColor;
			}else{
				specular = vec3(0.0,0.0,0.0);
			}
			
			//calculate color based on light results
			vec3 objectColor = vec3(0.0,0.0,1.0);
			vec3 result = (ambient + diffuse + specular) * objectColor;
			//vec3 result = objectColor;
			gl_FragColor = vec4(result, 1.0);
		}
		"""
		
		# initialize shaders
		super().__init__(vsCode, fsCode)
		
		# set default render values
		self.drawStyle = GL_TRIANGLES
		
		