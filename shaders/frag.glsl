#version 330 core

in vec3 fragNormal;
in vec3 frag_pos;

uniform vec3 material_color;
uniform vec3 specular_color;
uniform vec3 eye_pos;
uniform vec4 light_dir;
uniform int object_id;
uniform int light_id;

out vec4 outColor;

void main(){
    vec3 nor = normalize(fragNormal);
    nor = abs(nor);

    vec4 color = vec4(nor, 1.0);
    outColor = color;
}

void diffuseReflection(vec3 nor){
    if(light_id == 1)   light_dir = normalize(light_)
    color_diffuse_reflection = material_color * clamp(dot(nor, light_dir), 0, 1);
}

void specularReflection(vec3 nor) {

    color_specular_reflection = specular_color * pow(clamp(dot(nor, hal)))
}