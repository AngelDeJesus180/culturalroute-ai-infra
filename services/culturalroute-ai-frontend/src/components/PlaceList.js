function PlaceList({ places }) {
  return (
    <ul>
      {places.map(place => (
        <li key={place.id}>
          <h3>{place.name}</h3>
          <p>{place.description}</p>
        </li>
      ))}
    </ul>
  );
}

export default PlaceList;