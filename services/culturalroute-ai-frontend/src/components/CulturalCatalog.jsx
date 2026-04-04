import RecommendationMock from "./RecommendationMock";

function CulturalCatalog() {
  return (
    <div>
      <h1>CulturalRoute AI</h1>
      <h2>Catálogo de Lugares Culturales</h2>

      <h3>Museo Histórico</h3>
      <p>Lugar dedicado a la conservación del patrimonio cultural.</p>

      <h3>Teatro Municipal</h3>
      <p>Espacio cultural para eventos artísticos y escénicos.</p>

      <h3>Centro Cultural</h3>
      <p>Espacio para exposiciones y actividades culturales.</p>

      <RecommendationMock />
    </div>
  );
}

export default CulturalCatalog;