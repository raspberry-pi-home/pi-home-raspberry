import express from "express";
import helmet from "helmet";
import morgan from "morgan";

export const server = () => {
  const app: express.Application = express();
  const port: number = 3000;

  // db setup
  const low = require("lowdb");
  const FileSync = require("lowdb/adapters/FileSync");

  const adapter = new FileSync("db.json");
  const db = low(adapter);

  db.defaults({ devices: [] }).write();

  app.use(helmet());
  app.use(express.json());
  app.use(morgan("common"));

  app.get("/", (req, res) => {
    res.json({ body: "Hello World!" });
  });

  //todo
  /*
  abm dispositivo
    params pin, label, type
  list dispositivo
  actions
    turn off  turn on
  */
  app.get("/api/devices/", (req, res) => {
    res.json({
      body: db.get("devices").value(),
    });
  });

  app.get("/api/devices/:pin", (req, res) => {
    res.json({
      body: db.get("devices").find({ pin: req.params.pin }).value(),
    });
  });

  app.post("/api/devices/", (req, res) => {
    db.get("devices")
      .push({ pin: req.body.pin, label: req.body.label, type: req.body.type })
      .write();

    res.json({
      body: db.get("devices").find({ pin: req.body.pin }).value(),
    });
  });

  app.use((err: any, req: any, res: any, next: any) => {
    // eslint-disable-next-line no-console
    console.error(err.stack);
    res.status(500).send("Something went wrong!");
  });

  // eslint-disable-next-line no-console
  app.listen(port, () =>
    console.log(`App running on http://localhost:${port}`)
  );
};
