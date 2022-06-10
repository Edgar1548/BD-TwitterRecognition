export const Input = ({ onInputsChange, onInputsSubmit, listofInputs }) => {
  const handleChange = (event) => {
    const newinput = { ...listofInputs };
    newinput[event.target.name] = event.target.value;
    onInputsChange(newinput);
  };

  const handleSubmit = (event) => {
    fetch("/api/consult", {
      method: "POST",
      body: JSON.stringify({
        consult: listofInputs.consult,
        topk: listofInputs.topk,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        onInputsSubmit(data);
      });
  };

  return (
    <>
      <input
        name="consult"
        className="textarea__consult white"
        placeholder="Texto de la consulta"
        onChange={(e) => handleChange(e)}
      ></input>
      <div className="container__block">
        <input
          name="topk"
          className="white"
          placeholder="Tok K"
          onChange={(e) => handleChange(e)}
        />
        <button
          type="submit"
          className="white"
          onClick={(e) => handleSubmit(e)}
        >
          Buscar
        </button>
      </div>
    </>
  );
};
