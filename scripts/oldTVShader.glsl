#version 330 core

precision mediump float;
uniform sampler2D tex;
uniform float dst;
uniform float time;
uniform bool corridor;
uniform vec3 lightColor;
uniform float lightIntensity;
uniform float gamma;

in vec2 uvs;
out vec4 f_color;

void main() {
  // Old TV Effect
  vec2 center = vec2(0.5, 0.5);
  vec2 off_center = uvs - center;

  off_center *= 1.0 + 0.8 * pow(abs(off_center.yx), vec2(2.5));

  vec2 uvs2 = center+off_center;

  // If pixel is out of bounds (out of the "TV screen") we return black
  if (uvs2.x > 1.0 || uvs2.x < 0.0 ||
      uvs2.y > 1.0 || uvs2.y < 0.0) {
    f_color=vec4(0.0, 0.0, 0.0, 1.0);
  }
  else {
    // amount of chromatic aberration
    float chromatic_aberration = 0.015;

    // offset red and blue channels to ceate a chromatic aberration effect
    float r = texture(tex, uvs2 - vec2(chromatic_aberration * off_center)).x;
    float g = texture(tex, uvs2).y;
    float b = texture(tex, uvs2 + vec2(chromatic_aberration * off_center)).z;

    f_color = vec4(r, g, b, 1.0);
    // f_color = vec4(texture(tex, uvs2).rgb, 0);

    // Determine the brightness of the pixel
    float brightness = (f_color.r + f_color.g + f_color.b) / 5.0;

    // Apply a threshold to the brightness
    float threshold = 0.2;
    float alpha = smoothstep(threshold - 0.05, threshold + 0.05, brightness);

    // Blur the bright areas using a box filter
    float blurSize = 0.004;
    vec4 blur = vec4(0.0);
    for (int i = -4; i <= 4; i++) {
      blur += texture(tex, uvs2 + vec2(i, 0.0) * blurSize) * alpha / 9.0;
      blur += texture(tex, uvs2 + vec2(0.0, i) * blurSize) * alpha / 9.0;
    }

    // amount of blue that is mixed to the original image for bloom effect
    float mixAmount = 0.6;

    // color with blur applied
    f_color = mix(f_color, blur, mixAmount);

    // old TV stripes
    vec2 off_uvs = vec2(uvs.x * sin(uvs.y + time*0.1)*10, uvs.y);
    float fv = fract(uvs2.y/(10+sin(time)*0.1) * float(textureSize(tex,0).y));
    fv=min(1.0, 0.8+0.5*min(fv, 1.0-fv));

    // darken the color if it is in a "TV stripe"
    f_color.rgb*=fv;

    // apply gamma correction
    f_color.rgb = pow(f_color.rgb, vec3(1.0/gamma));

    if (corridor) {
      // apply colored overlay in corridor
      f_color.rgb += lightColor * lightIntensity;
    }

    if (dst < 500 && dst != 0) {
      f_color.r *= (-dst + 600)/100;
    }
  }
}