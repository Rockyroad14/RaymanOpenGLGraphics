#version 330 core

in vec2 fragUV;
uniform sampler2D tex;
out vec4 outColor;


void main(){

    vec3 color_tex = texture(tex, fragUV).rgb;

    outColor = vec4(color_tex, 1.0);
}


