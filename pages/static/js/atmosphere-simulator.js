/**
 * An atmosphere simulator, almost entirely based on the system by wwtyro:
 * https://github.com/wwwtyro/glsl-atmosphere/
 */

var Geometry = require('gl-geometry');
var glShader = require('gl-shader');

var vertexShader = require('../shaders/atmosphere.vert');
var fragmentShader = require('../shaders/atmosphere.frag');

function createAtmosphere(elm, params) {
  var docElement = elm;
  var canvas = document.createElement('canvas');
  canvas.width = params.width;
  canvas.height = params.height;
  // var aspectRatio = width/height;
  docElement.appendChild(canvas);

  var gl = canvas.getContext('webgl');
  gl.clearColor(0,0,0,0);

  var quad = Geometry(gl).attr('aPosition', [
    -1, -1, -1,
    1, -1, -1,
    1, 1, -1,
    -1, -1, -1,
    1, 1, -1,
    -1, 1, -1
  ]);

  var program = glShader(gl, vertexShader, fragmentShader);
  gl.clear(gl.COLOR_BUFFER_BIT);
  program.bind();
  quad.bind(program);

  program.uniforms.uSunPos = [0, Math.cos(params.starAngle) * 0.3 + 0.2, -1];
  program.uniforms.uSunIntensity = params.starIntensity;
  var sunColor = params.starColor;
  program.uniforms.uSunColor = [sunColor.red, sunColor.green, sunColor.blue];
  var rayleighCoefficients = params.rayleighCoefficients;
  program.uniforms.uRayleigh = [rayleighCoefficients.red, rayleighCoefficients.green, rayleighCoefficients.blue];
  program.uniforms.uScaleHeight = params.scaleHeight;
  program.uniforms.uAtmosphereDepth = params.atmosphereDepth;
  program.uniforms.uPlanetRadius = params.planetRadius;

  quad.draw();
};

var simulations = document.getElementsByClassName('atmosphere-simulation');
for(var s in simulations) {
  var simulationParams = JSON.parse(simulations[s].textContent);
  createAtmosphere(simulations[s].parentElement, simulationParams);
}
