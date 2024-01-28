class Req {
  #user_id = "7138599741986915329";
  #media_id = "7147953600210240002";

  constructor() {
    this.#start();
  }

  async #start() {
    const response = await fetch(
      "https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/comments?" +
        new URLSearchParams({
          group_id: this.#media_id,
          item_id: this.#media_id,
          media_id: this.#user_id,
          count: "1000",
          aid: "2657",
        }),
      {
        method: "GET",
        headers: {
          "User-Agent":
            "com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)",
        },
      }
    );
    const { data } = await response.json();
    const comments = data.data;

    comments.forEach(async (id) => {
      const response = await fetch(
        "https://api22-normal-useast1a.lemon8-app.com/api/550/comment_v2/detail?" +
          new URLSearchParams({
            group_id: this.#media_id,
            item_id: this.#media_id,
            media_id: this.#user_id,
            comment_id: "7148272678682493698",
            count: "6",
            dpi: "420",
            language: "en",
          }),
        {
          headers: {
            "User-Agent":
              "com.bd.nproject/55014 (Linux; U; Android 9; en_US; unknown; Build/PI;tt-ok/3.12.13.1)",
          },
        }
      );

      console.log(await response.json());
    });
  }
}

new Req();
