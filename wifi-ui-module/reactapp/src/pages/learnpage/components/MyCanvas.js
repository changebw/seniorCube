import * as THREE from 'three';

import { useEffect, useRef } from "react";

function Three() {
  const refContainer = useRef(null);
  let scene = new THREE.Scene();
  let camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  let renderer = new THREE.WebGLRenderer();
  let geometry = new THREE.BoxGeometry(2, 2, 2, 3, 3, 3);
  let material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
  let cube = new THREE.Mesh(geometry, material);

  renderer.setSize(500, 500);
  scene.add(cube);
  camera.position.z = 5;
  useEffect(() => {
    refContainer.current && refContainer.current.appendChild( renderer.domElement );
    function animate() {
        requestAnimationFrame( animate );
        renderer.render(scene, camera);
        cube.rotation.x += 0.02;
        cube.rotation.y += 0.02;
    }
    animate();
  });
  return (
    <div ref={refContainer}></div>
  );
}

export default Three;