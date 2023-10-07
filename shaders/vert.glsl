#version 330 core

in vec3 position;
in vec3 normal;

uniform mat4 model_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;

out vec3 fragNormal;
out vec3 frag_pos;

void main(){
    vec4 world_pos = model_matrix * vec4(position, 1.0);
    frag_pos = world_pos.xyz;
    gl_Position = projection_matrix * view_matrix * world_pos;
    mat4 normal_matrix = transpose(inverse(model_matrix));
    vec3 new_normal = (normal_matrix * vec4(normal, 0)).xyz;
    fragNormal = normalize(new_normal);
}

