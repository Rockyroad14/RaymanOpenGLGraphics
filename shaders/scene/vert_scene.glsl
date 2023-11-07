#version 420 core

// Attributes
layout (location = 0) in vec3 position;    // we can also use layout to specify the location of the attribute
layout (location = 2) in vec3 normal;


// todo: define all the out variables
out vec3 fragNormal;
out vec3 fragPos;
out vec4 fragPosLightSpace;

// todo: define all the uniforms
uniform mat4 model_matrix;
uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 light_view_matrix;
uniform mat4 light_projection_matrix;

void main(){
    // todo: fill in vertex shader
    // Tranform object to Center
    vec4 world_pos = model_matrix * vec4(position, 1.0);
    gl_Position = projection_matrix * view_matrix * world_pos;
    // Transform Normals
    mat4 normal_matrix = transpose(inverse(model_matrix));
    vec3 new_normal = (normal_matrix * vec4(normal, 0)).xyz;
    fragNormal = normalize(new_normal);

}