#version 330 core

in vec3 fragColor;
in vec2 fragUV;
uniform sampler2D tex;
out vec4 outColor;


void main(){
    vec3 normal = normalize(fragNormal);



    outColor = vec4(color, 1.0);
}


