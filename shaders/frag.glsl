#version 330 core

in vec3 fragNormal;

out vec4 outColor;

void main(){
    vec3 nor = normalize(fragNormal);
    nor = abs(nor);
    vec4 color = vec4(nor, 1.0);
    outColor = color;
}