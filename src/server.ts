import express from 'express'
import helmet from 'helmet'
import morgan from 'morgan'
import { Board } from 'pi-home-core'

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

  const setConfig = (config: object) => {
    const [valid, error] = board.validateConfig(config)
    if (!valid) {
      throw new Error(error)
    }

    board.setConfig(config)
  }

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
      pin: +req.body.pin,
      label: req.body.label,
      type: req.body.type,
    }

    const config = {
      devices: [...db.get('devices').value(), device],
      dependencies: db.get('dependencies').value(),
    }

    setConfig(config)

    db.get('devices').push(device).write()

    res.json(board.device(+req.body.pin))
  })

  // get a device
  app.get('/api/devices/:pin', (req, res) => {
    res.json(board.device(+req.params.pin))
  })

  // modify a device
  app.put('/api/devices/:pin', (req, res) => {
    let device = board.device(+req.params.pin)

    device = {
      pin: device.pin,
      label: req.body.label,
      type: req.body.type,
    }

    // @ts-ignore TS7006
    const devices = db.get('devices').filter(dbDevice => dbDevice.pin !== device.pin).value()

    const config = {
      devices: [...devices, device],
      dependencies: db.get('dependencies').value(),
    }

    setConfig(config)

    db.get('devices')
      .find({ pin: device.pin })
      .assign({ label: device.label, type: device.type })
      .write()

    res.json(board.device(device.pin))
  })

  // delete a device
  app.delete('/api/devices/:pin', (req, res) => {
    const device = board.device(+req.params.pin)

    // @ts-ignore TS7006
    const devices = db.get('devices').filter(dbDevice => dbDevice.pin !== device.pin).value()

    const config = {
      devices,
      dependencies: db.get('dependencies').value(),
    }

    setConfig(config)

    db.get('devices').remove({ pin: +req.params.pin }).write()

    res.json(board.devices())
  })

  // change device status (by pin)
  app.post('/api/change-status', (req, res) => {
    const status = board.changeStatus(+req.body.pin)

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

    setConfig(config)

    db.get('dependencies').push(dependency).write()

    res.json(dependency)
  })

  // get a dependency
  app.get('/api/dependencies/:pin', (req, res) => {
    const device = board.device(+req.params.pin)

    const directionTypes = board.availableTypesAndDirections()
    const direction = directionTypes[device.type]

    let devicePins = []
    if (direction == 'in') {
      devicePins = db.get('dependencies').filter({ inputPin: device.pin }).map('outputPin').value()
    } else {
      devicePins = db.get('dependencies').filter({ outputPin: device.pin }).map('inputPin').value()
    }

    const boardDevices = board.devices()
    // @ts-ignore TS7006
    const devices = devicePins.map(devicePin => boardDevices.find(boardDevice => boardDevice.pin === devicePin))

    res.json(devices)
  })

  // delete a dependency
  app.delete('/api/dependencies/:inputPin/:outputPin', (req, res) => {
    const dependency = db.get('dependencies').find({ inputPin: +req.params.inputPin, outputPin: +req.params.outputPin }).value()

    if (!!!dependency) {
      throw new Error('Dependency not found')
    }

    const config = {
      devices: db.get('devices').value(),
      // @ts-ignore TS7006
      dependencies: db.get('dependencies').filter(dbDependency =>
        !(dbDependency.inputPin === dependency.inputPin && dbDependency.outputPin === dependency.outputPin)
      ).value(),
    }

    setConfig(config)

    db.get('dependencies').remove({ inputPin: +req.params.inputPin, outputPin: +req.params.outputPin }).write()

    res.json(board.dependencies())
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
