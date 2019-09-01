from OpenGL.GL import *
from core import OpenGLUtils
from material import Material

#This material demonstrates specular lighting
#tutorial found online courtesy (https://learnopengl.com/Lighting/Basic-Lighting)
class WaterMaterial(Material):
	def __init__(self, color=[1,1,1], alpha=1, texture=None, isSpecular=0, useFog=0, fogStartDistance=5, fogEndDistance=15, fogColor=[1,1,1],useLight=0, clippingPlane=[0,-1,0,20]):
		#Code for the vertex shader
		
		#These shaders hope to improve on the basic specular light by using the light struct and built in lights from three py
		#rather than simple uniforms only
		
		vsCode = """
		in vec3 vertexPosition;
		in vec2 vertexUV;
		in vec3 vertexNormal;
		
		out vec3 position;
		out vec3 Normal;
		out vec3 regNormal;
		out vec2 UV;
		uniform mat4 projectionMatrix;
		uniform mat4 viewMatrix;
		uniform mat4 modelMatrix;
		
		out vec3 FragPos;
		
		out float cameraDistance;
		
		//shadow stuff
		uniform bool receiveShadow;
		uniform mat4 shadowProjectionMatrix;
		uniform mat4 shadowViewMatrix;
		out vec4 positionFromShadowLight;
		
		//water stuff
		//TODO: have this as an option for the water material
		uniform vec4 plane;
		
		void main(){			
			position = vec3( modelMatrix * vec4(vertexPosition, 1) );
            gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(vertexPosition, 1);
			//add clipping
			gl_ClipDistance[0] = dot(gl_Position, plane);
			cameraDistance=gl_Position.w;
			UV = vertexUV;
			if(receiveShadow){
				positionFromShadowLight = shadowProjectionMatrix * shadowViewMatrix * modelMatrix * vec4(vertexPosition,1);
			}
			//This line seems inefficient
			Normal = mat3(transpose(inverse(modelMatrix))) * vertexNormal;
			
			regNormal = normalize(mat3(modelMatrix)* vertexNormal);
			FragPos = vec3(modelMatrix * vec4(vertexPosition, 1));
		}
		"""
		
		#code for the fragment shader
		fsCode = """
		in vec3 position;
		in vec2 UV;
		in vec3 Normal;
		in vec3 regNormal;
		in vec3 FragPos;
		
		uniform vec3 viewPos;
		uniform vec3 viewDir;
		
		uniform vec3 color;
		uniform float alpha;
		
		//uniforms for loading images
		uniform bool useTexture;
		uniform sampler2D image;
		
		//uniforms for enabling/disabling different properties of the shader
		uniform bool isSpecular;
		uniform bool useFog;
		uniform bool receiveShadow;
		uniform bool useLight;
		
		//fog calculation
		uniform vec3 fogColor;
		uniform float fogStartDistance;
		uniform float fogEndDistance;
		in float cameraDistance;
		
		
		//shadowCalculation
		in vec4 positionFromShadowLight;
		uniform sampler2D shadowMap;
		uniform float shadowStrength;
		uniform float shadowBias;
		uniform vec3 shadowLightDirection;
		
		
		
		//struct for the light objects
		struct Light{
			bool isAmbient;
			bool isDirectional;
			bool isPoint;
			
			//used by all lights
			float strength;
			vec3 color;
			
			//used by point lights only
			vec3 position;
			
			//used by directional lights only
			vec3 direction;
		};
		
		uniform Light light0;//using nomenclature of three py for the lights
		uniform Light light1;
		uniform Light light2;
		uniform Light light3;
		
		void main(){
			//TODO: move declared variables to uniforms when convenient/needed
			//vec3 objectColor = vec3(0.0,1.0,0.0);
			//vec3 objectColor = color;
			vec4 baseColor = vec4(color, alpha);
			//change color according to texture
			if(useTexture){
				baseColor *= texture2D(image, UV);
			}
			
			//variables to be used inside the loop
			vec3 lightDir;
			vec3 diffuse;
			vec3 norm = normalize(Normal);
			
			vec3 totalLight = vec3(0.0,0.0,0.0);//the total amount of light in any one spot
			
			Light lightArray[4] = {light0, light1, light2, light3};//array for the lights
			
			//store the ambient light seperately, if the object is lit more than the ambience, take it away
			vec3 ambient = vec3(0.0,0.0,0.0);
			if(useLight){
				for(int n = 0;n < 4; n++){
					//get the light
					Light light = lightArray[n];
					if(light.isAmbient){
						totalLight = totalLight + (light.strength * light.color);
						//save value in ambient, for later calculation
						ambient = light.strength * light.color;
					}else if (light.isDirectional){
						//diffuse lighting
						//float diffuseStrength = 0.5;
						lightDir = -light.direction;
						float diff = max(dot(norm, lightDir),0.0);
						diffuse = diff * light.color * light.strength;
						
						//specular
						vec3 specular;
						
						if(isSpecular){
							float specularStrength = 0.5;
							vec3 reflectDir = reflect(-lightDir, norm);
							float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16);
							specular = light.strength * spec * light.color;
						}else{
							specular = vec3(0,0,0);
						}
						
						totalLight = totalLight + (diffuse + specular);
					}else if(light.isPoint){
						//diffuse
						float diffuseStrength = 0.5;
						lightDir = normalize(light.position - FragPos);
						float diff = max(dot(norm, lightDir), 0.0);
						diffuse = diff * light.strength * light.color;
						
						//specular
						vec3 specular;
						
						if(isSpecular){
							float specularStrength = 0.5;
							vec3 reflectDir = reflect(-lightDir, norm);
							float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
							specular = light.strength * spec * light.color;
						}else{
							specular = vec3(0,0,0);
						}
						
						totalLight = totalLight + (diffuse + specular);
					}
				}
			}else{
				totalLight = vec3(1,1,1);
				ambient = vec3(1,1,1);
			}
			
			//calculate shadows
			if(receiveShadow){
				//norm is unitNormal
				float cosAngle = dot(norm, shadowLightDirection);
				bool facingLight = (cosAngle < -0.05);
				vec3 shadowCoord = (positionFromShadowLight.xyz / positionFromShadowLight.w) / 2.0 + 0.5;
				float closestDistanceToLight = texture2D(shadowMap, shadowCoord.xy).r;
				float fragmentDistanceToLight = shadowCoord.z;
				
				if(facingLight && fragmentDistanceToLight > closestDistanceToLight + shadowBias){
					baseColor *= vec4(shadowStrength,shadowStrength, shadowStrength,1.0);
				}
			}
			
			//take away ambient light
			vec3 noAmbience = totalLight - ambient;
			
			//take away again, the result should be all positive if there is more than the ambient amount of light;
			vec3 greaterThanAmbience = noAmbience - ambient;
			
			if(length(noAmbience) > length(ambient)){
				totalLight = noAmbience;
			}else{
				totalLight = ambient;
			}
			
			
			
			
			//calculate color based on light results
			//vec3 result = (ambient + totalLight) * objectColor;
			vec4 result = vec4(totalLight,1.0) * baseColor;
			
			//add fog effect if necessary
			if(useFog){
				float fogFactor = clamp((fogEndDistance - cameraDistance)/(fogEndDistance - fogStartDistance),0.0,1.0);
				result = mix(vec4(fogColor,1.0),result, fogFactor);
			}
			
			//vec3 result = objectColor;
			//gl_FragColor = vec4(result, alpha);
			gl_FragColor = result;
		}
		"""
		
		# initialize shaders
		super().__init__(vsCode, fsCode)
		
		# set default uniform values
		self.setUniform( "vec3", "color", color )
		self.setUniform( "float", "alpha", alpha )
		
		#fog
		self.setUniform( "float", "fogStartDistance", fogStartDistance )
		self.setUniform( "float", "fogEndDistance", fogEndDistance )
		self.setUniform( "vec3", "fogColor", fogColor )
		self.setUniform( "bool", "useFog", useFog )
		
		#clipping
		self.setUniform("vec4","plane",clippingPlane)
		
		self.setUniform("bool","isSpecular", isSpecular)
		
		self.setUniform("bool","useLight", useLight)
		
		if texture is None:
			self.setUniform("bool", "useTexture",0)
			self.setUniform("sampler2D","image",-1)
		else:
			self.setUniform("bool","useTexture",1);
			self.setUniform("sampler2D","image",texture)
		
		# set default render values
		self.drawStyle = GL_TRIANGLES
		
		