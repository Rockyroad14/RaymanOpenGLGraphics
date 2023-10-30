#version 420 core

// todo: define all the input variables to the fragment shader
in vec3 fragPos;
in vec3 fragNormal;
in vec4 fragPosLightSpace;

// todo: define all the uniforms
uniform vec3 material_color;
uniform vec3 light_pos;



layout (binding=0) uniform sampler2D depthTex;  // depth texture bound to texture unit 0
out vec4 outColor;

void main(){
    // todo: fill in the fragment shader
    // Making the light postion a 3D coordinate
    vec4 light_pos = vec4(light_pos, 1.0);
    vec3 normal = normalize(fragNormal);
    vec3 light_dir = normalize(light_pos.xyz-fragPos);
    vec3 color_diffuse_reflection = material_color * clamp(dot(normal, light_dir), 0, 1);

    // Shadow Stuff
    vec3 fragPos3D = fragPosLightSpace.xyz / fragPosLightSpace.w;
    fragPos3D = (fragPos3D + 1.0) / 2.0;
    float z_current = fragPos3D.z;
    float z_depthTex = texture(depthTex, fragPos3D.xy).r;

    if(z_current > z_depthTex)
    {
        outColor = vec4(0.0, 0.0, 0.0, 0.0);
    }
    else
    {
        outColor = vec4(color_diffuse_reflection, 1.0);
    }


}