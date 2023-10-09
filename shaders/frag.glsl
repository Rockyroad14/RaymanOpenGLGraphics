#version 330 core

in vec3 fragNormal;
in vec3 frag_pos;

uniform vec3 material_color;
uniform vec3 specular_color;
uniform vec3 eye_pos;

out vec4 outColor;

void main(){
    vec3 nor = normalize(fragNormal);
    nor = abs(nor);
    vec4 color = vec4(nor, 1.0);
    outColor = color;
}