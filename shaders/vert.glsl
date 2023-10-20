#version 440 core

in vec3 position;
in vec3 normal;
in vec2 uv;

uniform mat4 model_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;

out vec2 fragUV;
out vec3 frag_pos;
out vec3 fragNormal;

void main(){
    vec4 world_pos = model_matrix * vec4(position, 1.0);
    frag_pos = world_pos.xyz;
    gl_Position = projection_matrix * view_matrix * world_pos;
    mat4 normal_matrix = inverse(transpose(model_matrix));
    vec3 new_normal = (normal_matrix * vec4(normal, 0)).xyz;

    fragNormal = new_normal;
    fragUV = uv;
}

