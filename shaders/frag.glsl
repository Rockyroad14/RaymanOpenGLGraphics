#version 440 core
in vec3 frag_pos;
in vec2 fragUV;
in vec3 fragNormal;
layout (binding=0) uniform sampler2D tex;
layout (binding=1) uniform samplerCube cubeMapTex;
uniform vec3 eye_pos;
uniform int textype;
out vec4 outColor;

vec3 environmentMapping()
{
    vec3 fragPos = normalize(frag_pos);
    vec3 N = normalize(fragNormal);
    // Calculate view.
    vec3 V = normalize(eye_pos - fragPos);
    vec3 Reflect = reflect(-V, N);
    vec3 color_env = texture(cubeMapTex, Reflect).rgb;

    return color_env;
}


void main(){
    vec3 color;

    vec3 color_env = environmentMapping();
    vec3 color_tex = texture(tex, fragUV).rgb;

    switch (textype) {
        case 1:
            color = color_env;
            break;
        case 2:
            color = color_tex;
            break;
        case 3:
            color = mix(color_tex, color_env, 0.5);
            break;
    }

    outColor = vec4(color, 1.0);
}


