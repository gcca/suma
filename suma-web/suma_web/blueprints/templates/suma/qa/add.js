(function () {
  const form = document.getElementById("id-add-form");
  if (form instanceof HTMLFormElement) {
    form.querySelectorAll("input").forEach((el) =>
      el.addEventListener("keydown", (evt) => {
        if (evt.key == "Enter") {
          evt.preventDefault();
          if (evt.ctrlKey || evt.metaKey) {
            form.submit();
          }
        }
      })
    );
    form.querySelectorAll("textarea").forEach((el) =>
      el.addEventListener("keydown", (evt) => {
        if ((evt.ctrlKey || evt.metaKey) && evt.key == "Enter") {
          evt.preventDefault();
          form.submit();
        }
      })
    );
  } else {
    throw new Error("cannot find id-add-form");
  }
})();
