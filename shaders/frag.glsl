#version 330 core

in vec3 fragNormal;
in vec3 frag_pos;
out vec4 outColor;
uniform vec3 material_color;
uniform vec4 light_pos;
uniform vec3 eye_pos;
uniform float ambient_intensity;
uniform bool silhouette;
uniform int toon;

vec3 silhouetteEdge(vec3 color)
{
    if (silhouette)
    {
        vec3 view_dir = normalize(eye_pos - frag_pos);
        if(dot(fragNormal, view_dir) < 0.2)
        {
            color = vec3(0, 0, 0);
        }
    }

    return color;
}

vec3 toonShading(vec3 light_dir)
{
    float intensity = clamp(dot(light_dir, fragNormal), 0, 1);
    int n = 5;
    float step = sqrt(intensity) * n;
    intensity = (floor(step) + smoothstep(0.48, 0.52, fract(step))) / n;
    intensity = intensity * intensity;
    vec3 color = material_color * intensity;
    color = silhouetteEdge(color);
    return color;
}



void main(){
    vec3 normal = normalize(fragNormal);

    //Diffuse
    vec3 light_dir;
    if (light_pos.w==0.0)   light_dir = normalize(light_pos.xyz);                   // directional light
    else                    light_dir = normalize(light_pos.xyz-frag_pos);      // point light
    vec3 color = material_color * clamp(dot(normal, light_dir), 0, 1);

    if(toon == 2)
    {
        color = toonShading(light_dir);
    }

    outColor = vec4(color, 1.0);
}


