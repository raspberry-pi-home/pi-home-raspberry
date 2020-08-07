import express from 'express'

// @ts-ignore TS7006
export const api = (db, board) => {
  const router = express.Router()

  const setConfig = (config: object) => {
    const [valid, error] = board.validateConfig(config)
    if (!valid) {
      throw new Error(error)
    }

    board.setConfig(config)
  }

  // list all devices
  router.get('/devices', (req, res) => {
    const devices = board.devices()

    if (req.query?.type === 'led' || req.query?.type === 'button') {
      // @ts-ignore TS7006
      return res.json(devices.filter(device => device.type && device.type.toLowerCase().endsWith(req.query.type)))
    }

    if (req.query?.type === 'configured') {
      // @ts-ignore TS7006
      return res.json(devices.filter(device => device.type))
    } else if (req.query?.type === 'available') {
      // @ts-ignore TS7006
      const pins = devices.filter(device => !device.type).map(device => device.pin)

      // @ts-ignore TS7006
      const types = board.availableDeviceTypes.reduce((memo, type) => ({ ...memo, [type]: pins }), {})

      return res.json(types)
    }

    res.json(devices)
  })

  // create a device
  router.post('/devices', (req, res) => {
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
  router.get('/devices/:pin', (req, res) => {
    res.json(board.device(+req.params.pin))
  })

  // modify a device
  router.put('/devices/:pin', (req, res) => {
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
  router.delete('/devices/:pin', (req, res) => {
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
  router.post('/change-status', (req, res) => {
    const status = board.changeStatus(+req.body.pin)

    res.json({ status })
  })

  // link an input device to an output device
  router.post('/devices/link/:inputPin/:outputPin', (req, res) => {
    const dependency = {
      inputPin: +req.params.inputPin,
      outputPin: +req.params.outputPin,
    }

    const config = {
      devices: db.get('devices').value(),
      dependencies: [...db.get('dependencies').value(), dependency],
    }

    setConfig(config)

    db.get('dependencies').push(dependency).write()

    res.json(dependency)
  })

  // unlink an input device from the output device
  router.post('/devices/unlink/:inputPin/:outputPin', (req, res) => {
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

    res.json(dependency)
  })

  // debug
  router.get('/_debug', (req, res) => {
    res.json({
      board,
      db,
    })
  })

  return router
}
