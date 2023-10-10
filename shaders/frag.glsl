#version 330 core

in vec3 fragNormal;
in vec3 frag_pos;
out vec4 outColor;
uniform vec3 material_color;
uniform vec4 light_pos;
uniform vec3 eye_pos;
uniform int shininess;
uniform vec3 specular_color;
uniform float ambient_intensity;
uniform float K_s;


void main(){
    vec3 normal = normalize(fragNormal);

    //Diffuse
    vec3 light_dir;
    if (light_pos.w==0.0)   light_dir = normalize(light_pos.xyz);                   // directional light
    else                    light_dir = normalize(light_pos.xyz-frag_pos);      // point light
    vec3 color_diffuse_reflection = material_color * clamp(dot(normal, light_dir), 0, 1);

    //Specular
    vec3 view_dir = normalize(eye_pos - frag_pos);
    vec3 half_vector = normalize(light_dir + view_dir);
    vec3 color_specular_reflection = specular_color * pow(clamp(dot(normal, half_vector), 0, 1), shininess);

    //combo of diffuse and specular
    vec3 color_ambient_light = ambient_intensity * material_color;
    vec3 color = color_ambient_light + color_diffuse_reflection + K_s * color_specular_reflection;


    outColor = vec4(color, 1.0 );
}


