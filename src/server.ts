import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'
import { Board, validateConfig } from 'pi-home-core'

export const server = () => {
  // app setup
  const app: express.Application = express()
  const port: number = 3000

  app.use(helmet())
  app.use(express.json())
  app.use(morgan('common'))

  // db setup
  const low = require('lowdb')
  const FileSync = require('lowdb/adapters/FileSync')

  const adapter = new FileSync('db.json')
  const db = low(adapter)

  db.defaults({
    devices: [],
    dependencies: [],
  }).write()

  // board setup
  const board = new Board()
  board.setConfig({
    devices: db.get('devices').value(),
    dependencies: db.get('dependencies').value(),
  })

  // routes setup
  app.get('/', (req, res) => {
    res.send('Welcome to raspberry-pi-home!')
  })

  // list all devices
  app.get('/api/devices', (req, res) => {
    res.json(board.devices())
  })

  // create a device
  app.post('/api/devices', (req, res) => {
    const device = {
      pin: req.body.pin,
      label: req.body.label,
      type: req.body.type,
    }

    const config = {
      devices: [...db.get('devices').value(), device],
      dependencies: db.get('dependencies').value(),
    }

    const error = validateConfig(config)

    if (error) {
      throw new Error(error)
    }

    board.setConfig(config)

    db.get('devices').push(device).write()

    // TODO get device from board?
    res.json(device)
  })

  // get a device
  app.get('/api/devices/:pin', (req, res) => {
    const device = db.get('devices').find({ pin: +req.params.pin }).value()

    // TODO verify this
    if (!!!device) {
      throw new Error('Device not found')
    }

    //TODO get device from board?
    res.json(device)
  })

  // modify a device
  app.put('/api/devices/:pin', (req, res) => {
    let device = db.get('devices').find({ pin: +req.params.pin }).value()

    // TODO verify this
    if (!!!device) {
      throw new Error('Device not found')
    }

    device = {
      pin: device.pin,
      label: req.body.label,
      type: req.body.type,
    }

    // TODO merge device
    const config = {
      devices: [...db.get('devices').value(), device],
      dependencies: db.get('dependencies').value(),
    }

    const error = validateConfig(config)

    if (error) {
      throw new Error(error)
    }

    board.setConfig(config)

    db.get('devices')
      .find({ pin: device.pin })
      .assign({ label: device.label, type: device.type })
      .write()

    // TODO get device from board?
    res.json(device)
  })

  // delete a device
  app.delete('/api/devices/:pin', (req, res) => {
    const device = db.get('devices').find({ pin: +req.params.pin }).value()

    // TODO verify this
    if (!!!device) {
      throw new Error('Device not found')
    }

    // TODO remove device
    const config = {
      devices: [...db.get('devices').value(), device],
      dependencies: db.get('dependencies').value(),
    }

    const error = validateConfig(config)

    if (error) {
      throw new Error(error)
    }

    board.setConfig(config)

    db.get('devices').remove({ pin: +req.params.pin }).write()

    // TODO get device from board?
    res.json(device)
  })

  // change device status (by pin)
  app.post('/api/change-status', (req, res) => {
    let device = db.get('devices').find({ pin: req.body.pin }).value()

    // TODO verify this
    if (!!!device) {
      throw new Error('Device not found')
    }

    // TODO handle error
    const status = board.changeStatus(req.body.pin)

    // TODO get device from board?
    res.json({ status })
  })

  // list all dependencies
  app.get('/api/dependencies', (req, res) => {
    res.json(board.dependencies())
  })

  // create a dependency
  app.post('/api/dependencies', (req, res) => {
    const dependency = {
      inputPin: req.body.inputPin,
      outputPin: req.body.outputPin,
    }

    const config = {
      devices: db.get('devices').value(),
      dependencies: [...db.get('dependencies').value(), dependency],
    }

    const error = validateConfig(config)

    if (error) {
      throw new Error(error)
    }

    board.setConfig(config)

    db.get('dependencies').push(dependency).write()

    // TODO get dependency from board?
    res.json(dependency)
  })

  // get a dependency
  app.get('/api/dependencies/:pin', (req, res) => {
    const device = db.get('devices').find({ pin: +req.params.pin }).value()

    // TODO verify this
    if (!!!device) {
      throw new Error('Device for dependency not found')
    }

    const directionTypes = board.availableTypesAndDirections()
    const direction = directionTypes[device.type]

    if (direction == 'in') {
      return res.json(db.get('dependencies').find({ outputPin: req.params.pin }).value())
    }

    res.json(db.get('dependencies').find({ inputPin: req.params.pin }).value())
  })

  // delete a dependency
  app.delete('/api/dependencies/:inputpin/:outputpin', (req, res) => {
    const dependency = db.get('dependencies').find({ inputPin: req.params.inputPin, outputPin: req.params.outputPin }).value()

    // TODO verify this
    if (!!!dependency) {
      throw new Error('Dependency not found')
    }

    db.get('dependencies').remove({ inputPin: req.params.inputPin, outputPin: req.params.outputPin }).write()

    res.json(dependency)
  })

  app.use((err: any, req: any, res: any, next: any) => {
    if (process.env.DEBUG) {
      // eslint-disable-next-line no-console
      console.error(err.stack)
    }
    res.status(500).send(err.message)
  })

  app.listen(port, () =>
    // eslint-disable-next-line no-console
    console.log(`App running on http://localhost:${port}`)
  )
}
