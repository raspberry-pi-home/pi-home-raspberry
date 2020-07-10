import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'
import { Board } from 'pi-home-core'

export const server = () => {
  const app: express.Application = express()
  const port: number = 3000

  // db setup
  const low = require('lowdb')
  const FileSync = require('lowdb/adapters/FileSync')

  const adapter = new FileSync('db.json')
  const db = low(adapter)

  db.defaults({ devices: [], dependencies: [] }).write()

  app.use(helmet())
  app.use(express.json())
  app.use(morgan('common'))

  app.get('/', (req, res) => {
    res.json({ body: 'Hello World!' })
  })

  //TODO llenar
  const board = new Board({
    devices: [],
    dependencies: [],
  })

  /* Devices */
  app.get('/api/devices', (req, res) => {
    res.json(board.devices())
  })

  app.get('/api/devices/:pin', (req, res) => {
    res.json(db.get('devices').find({ pin: req.params.pin }).value())
  })

  app.post('/api/devices', (req, res) => {
    const device = {
      pin: req.body.pin,
      label: req.body.label,
      type: req.body.type,
    }

    board.validateDevice(device, db.get('devices').value())

    db.get('devices').push(device).write()
    //TODO obtener device desde board?
    res.json(device)
  })

  app.put('/api/devices/:pin', (req, res) => {
    const device = {
      pin: req.params.pin,
      label: req.body.label,
      type: req.body.type,
    }
    board.validateDevice(device, db.get('devices').value())
    db.get('devices')
      .find({ pin: req.params.pin })
      .assign({ label: req.body.label, type: req.body.type })
      .write()

    //TODO obtener device desde board?
    res.json(device)
  })

  app.delete('/api/devices/:pin', (req, res) => {
    const device = {
      pin: req.params.pin,
      label: req.body.label,
      type: req.body.type,
    }

    db.get('devices').remove({ pin: req.params.pin }).write()
    //TODO obtener device desde board?
    res.end()
  })

  app.post('/api/change-status', (req, res) => {
    const status = board.changeStatus(req.body.pin)
    res.json({ status })
  })

  /*Dependencies*/
  app.get('/api/dependencies', (req, res) => {
    res.json(db.get('dependencies').value())
  })

  app.get('/api/dependencies/:pin', (req, res) => {
    const device = db.get('devices').find({ pin: req.params.pin })
    const directionTypes = board.availableTypesAndDirections()
    const direction = directionTypes[device.type]

    if (direction == 'in') {
      res.json(
        db.get('dependencies').find({ outputPin: req.params.pin }).value()
      )
    }

    res.json(db.get('dependencies').find({ inputPin: req.params.pin }).value())
  })

  app.post('/api/dependencies', (req, res) => {
    const dependency = {
      inputPin: req.body.inputPin,
      outputPin: req.body.outputPin,
    }

    db.get('dependencies').push(dependency)
    res.json(dependency)
  })

  app.delete('/api/dependencies/:inputpin/:outputpin', (req, res) => {
    db.get('dependencies')
      .remove({
        inputPin: req.params.inputPin,
        outputPin: req.params.outputPin,
      })
      .write()
    res.end()
  })

  app.use((err: any, req: any, res: any, next: any) => {
    // eslint-disable-next-line no-console
    console.error(err.stack)
    res.status(500).send('Something went wrong!')
  })

  app.listen(port, () =>
    // eslint-disable-next-line no-console
    console.log(`App running on http://localhost:${port}`)
  )
}
