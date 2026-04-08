import RecommendationMock from "./RecommendationMock";
import PlaceList from "./PlaceList";
import places from "../data/places";

function CulturalCatalog() {
  return (
    <div>
      <h1>CulturalRoute AI</h1>
      <h2>Catálogo de Lugares Culturales</h2>

      <PlaceList places={places} />

      <RecommendationMock />
    </div>
  );
}

export default CulturalCatalog;