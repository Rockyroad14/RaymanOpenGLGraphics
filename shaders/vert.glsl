#version 330 core

in vec3 position;
in vec2 uv;

uniform mat4 model_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;

out vec2 fragUV;

void main(){
    vec4 world_pos = model_matrix * vec4(position, 1.0);
    gl_Position = projection_matrix * view_matrix * world_pos;
    fragUV = uv;
}

