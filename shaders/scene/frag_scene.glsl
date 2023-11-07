#version 420 core

// todo: define all the input variables to the fragment shader
in vec3 fragPos;
in vec3 fragNormal;
in vec3 viewVector;
in vec4 fragPosLightSpace;

// todo: define all the uniforms
uniform vec3 material_color;
uniform vec3 light_pos;


 // depth texture bound to texture unit 0
out vec4 outColor;



void main(){
    // todo: fill in the fragment shader
    // Making the light postion a 3D coordinate
    vec4 light_pos = vec4(light_pos, 1.0);
    vec3 normal = normalize(fragNormal);
    vec3 light_dir = normalize(light_pos.xyz-fragPos);


}