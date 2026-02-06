self.onmessage = function(event) {
  // Simula cómputo distribuido para tareas
  const result = event.data * 2;
  self.postMessage(result);
};
